from __future__ import absolute_import

from django.db import models
from django.conf import settings
from django.db import transaction, connection
from django.template.defaultfilters import slugify

from treebeard.exceptions import InvalidMoveToDescendant, PathOverflow

from fancypages import manager
from fancypages import abstract_models

Category = models.get_model('catalogue', 'Category')


class FancyPage(Category, abstract_models.AbstractFancyPage):
    objects = manager.PageManager()

    @models.permalink
    def get_absolute_url(self):
        # make sure that the home view is actually redirecting to '/'
        # and not to '/home/'.
        if self.slug == slugify(getattr(settings, 'FP_HOMEPAGE_NAME')):
            return ('home', (), {})
        return ('fancypages:page-detail', (), {'slug': self.slug})

    def add_child(self, **kwargs):
        """
        Adds a child to the node.

        :raise PathOverflow: when no more child nodes can be added
        """

        if not self.is_leaf() and self.node_order_by:
            # there are child nodes and node_order_by has been set
            # delegate sorted insertion to add_sibling
            return self.get_last_child().add_sibling('sorted-sibling',
                                                     **kwargs)

        # creating a new object
        newobj = self.__class__(**kwargs)
        newobj.depth = self.depth + 1
        print Category.objects.all()
        if not self.is_leaf():
            # adding the new child as the last one
            newobj.path = self._inc_path(self.get_last_child().path)
        else:
            # the node had no children, adding the first child
            newobj.path = self._get_path(self.path, newobj.depth, 1)
            if len(newobj.path) > \
                    newobj.__class__._meta.get_field('path').max_length:
                raise PathOverflow('The new node is too deep in the tree, try'
                                   ' increasing the path.max_length property'
                                   ' and UPDATE your  database')
        # saving the instance before returning it
        newobj.save()
        newobj._cached_parent_obj = self

        # we increase the numchild value of the object in memory, but can't
        # save because that makes this django 1.0 compatible code explode
        self.numchild += 1

        # we need to use a raw query
        sql = "UPDATE {table} SET numchild=numchild+1 WHERE path=%s".format(
               table=connection.ops.quote_name(self.category_ptr.__class__._meta.db_table)
        )
        cursor = connection.cursor()
        cursor.execute(sql, [self.path])
        transaction.commit_unless_managed()

        return newobj

    def delete(self):
        "Removes a node and all it's descendants."
        self.__class__.objects.filter(id=self.id).delete()
        FancyPage.fix_tree()

    @classmethod
    def fix_tree(cls, destructive=False):
        if destructive:
            dump = cls.dump_bulk(None, True)
            cls.objects.all().delete()
            cls.load_bulk(dump, None, True)
        else:
            table_name = Category._meta.db_table
            cursor = connection.cursor()

            # fix the depth field
            # we need the WHERE to speed up postgres
            sql = "UPDATE %s " \
                    "SET depth=LENGTH(path)/%%s " \
                  "WHERE depth!=LENGTH(path)/%%s" % (
                      connection.ops.quote_name(table_name), )
            vals = [cls.steplen, cls.steplen]
            cursor.execute(sql, vals)

            # fix the numchild field
            vals = ['_' * cls.steplen]
            # the cake and sql portability are a lie
            if cls.get_database_engine() == 'mysql':
                sql = "SELECT tbn1.path, tbn1.numchild, (" \
                              "SELECT COUNT(1) " \
                              "FROM %(table)s AS tbn2 " \
                              "WHERE tbn2.path LIKE " \
                                "CONCAT(tbn1.path, %%s)) AS real_numchild " \
                      "FROM %(table)s AS tbn1 " \
                      "HAVING tbn1.numchild != real_numchild" % {
                        'table': connection.ops.quote_name(table_name)}
            else:
                subquery = "(SELECT COUNT(1) FROM %(table)s AS tbn2" \
                           " WHERE tbn2.path LIKE tbn1.path||%%s)"
                sql = "SELECT tbn1.path, tbn1.numchild, " + subquery + " " \
                      "FROM %(table)s AS tbn1 " \
                      "WHERE tbn1.numchild != " + subquery
                sql = sql % {
                        'table': connection.ops.quote_name(table_name)}
                # we include the subquery twice
                vals *= 2
            cursor.execute(sql, vals)
            sql = "UPDATE %(table)s " \
                     "SET numchild=%%s " \
                   "WHERE path=%%s" % {
                     'table': connection.ops.quote_name(table_name)}
            for node_data in cursor.fetchall():
                vals = [node_data[2], node_data[0]]
                cursor.execute(sql, vals)

            transaction.commit_unless_managed()

    def move(self, target, pos=None):
        """
        Moves the current node and all it's descendants to a new position
        relative to another node.

        :raise PathOverflow: when the library can't make room for the
           node's new position
        """

        pos = self._fix_move_opts(pos)

        oldpath = self.path

        # initialize variables and if moving to a child, updates "move to
        # child" to become a "move to sibling" if possible (if it can't
        # be done, it means that we are  adding the first child)
        pos, target, newdepth, siblings, newpos = self._fix_move_to_child(pos,
            target, target.depth)

        if target.is_descendant_of(self):
            raise InvalidMoveToDescendant("Can't move node to a descendant.")

        if oldpath == target.path and (
              (pos == 'left') or \
              (pos in ('right', 'last-sibling') and \
                target.path == target.get_last_sibling().path) or \
              (pos == 'first-sibling' and \
                target.path == target.get_first_sibling().path)):
            # special cases, not actually moving the node so no need to UPDATE
            return

        if pos == 'sorted-sibling':
            siblings = self.get_sorted_pos_queryset(
                target.get_siblings(), self)
            try:
                newpos = self._get_lastpos_in_path(siblings.all()[0].path)
            except IndexError:
                newpos = None
            if newpos is None:
                pos = 'last-sibling'

        stmts = []
        # generate the sql that will do the actual moving of nodes
        oldpath, newpath = self._move_add_sibling_aux(pos, newpos, newdepth,
            target, siblings, stmts, oldpath, True)
        print stmts
        # updates needed for mysql and children count in parents
        self._updates_after_move(oldpath, newpath, stmts)

        print stmts

        cursor = connection.cursor()
        for sql, vals in stmts:
            cursor.execute(sql, vals)
        transaction.commit_unless_managed()

    @classmethod
    def _get_sql_newpath_in_branches(cls, oldpath, newpath):
        sql1 = "UPDATE %s SET" % (
            connection.ops.quote_name(Category._meta.db_table), )

        # <3 "standard" sql
        if cls.get_database_engine() == 'sqlite3':
            # I know that the third argument in SUBSTR (LENGTH(path)) is
            # awful, but sqlite fails without it:
            # OperationalError: wrong number of arguments to function substr()
            # even when the documentation says that 2 arguments are valid:
            # http://www.sqlite.org/lang_corefunc.html
            sqlpath = "%s||SUBSTR(path, %s, LENGTH(path))"
        elif cls.get_database_engine() == 'mysql':
            # hooray for mysql ignoring standards in their default
            # configuration!
            # to make || work as it should, enable ansi mode
            # http://dev.mysql.com/doc/refman/5.0/en/ansi-mode.html
            sqlpath = "CONCAT(%s, SUBSTR(path, %s))"
        else:
            sqlpath = "%s||SUBSTR(path, %s)"

        sql2 = ["path=%s" % (sqlpath, )]
        vals = [newpath, len(oldpath) + 1]
        if (len(oldpath) != len(newpath) and
                cls.get_database_engine() != 'mysql'):
            # when using mysql, this won't update the depth and it has to be
            # done in another query
            # doesn't even work with sql_mode='ANSI,TRADITIONAL'
            # TODO: FIND OUT WHY?!?? right now I'm just blaming mysql
            sql2.append("depth=LENGTH(%s)/%%s" % (sqlpath, ))
            vals.extend([newpath, len(oldpath) + 1, cls.steplen])
        sql3 = "WHERE path LIKE %s"
        vals.extend([oldpath + '%'])
        sql = '%s %s %s' % (sql1, ', '.join(sql2), sql3)
        return sql, vals

    @classmethod
    def _get_sql_update_depth_in_branch(cls, path):
        """
        :returns: The sql needed to update the depth of all the nodes in a
                  branch.
        """

        # Right now this is only used by *sigh* mysql.
        sql = "UPDATE %s SET depth=LENGTH(path)/%%s" \
              " WHERE path LIKE %%s" % (
                  connection.ops.quote_name(Category._meta.db_table), )
        vals = [cls.steplen, path + '%']
        return sql, vals

    @classmethod
    def _get_sql_update_numchild(cls, path, incdec='inc'):
        ":returns: The sql needed the numchild value of a node"
        sql = "UPDATE %s SET numchild=numchild%s1" \
              " WHERE path=%%s" % (
                connection.ops.quote_name(Category._meta.db_table),
                {'inc': '+', 'dec': '-'}[incdec])
        vals = [path]
        return sql, vals


# We have to import all models from django-fancypages AFTER re-defining
# FancyPage because otherwise we'll import it FancyPage first and will use
# the wrong one.
from fancypages.models import (
    FancyPage,
    VisibilityType,
    PageType,
    Container,
    OrderedContainer,
    ImageMetadataMixin,
    NamedLinkMixin,
    TabBlock,
    TwoColumnLayoutBlock,
    ThreeColumnLayoutBlock,
    FourColumnLayoutBlock,
    ContentBlock,
    TextBlock,
    TitleTextBlock,
    PageNavigationBlock,
    PrimaryNavigationBlock,
    VideoBlock,
    TwitterBlock
)


from .product import (
    SingleProductBlock,
    HandPickedProductsPromotionBlock,
    AutomaticProductsPromotionBlock,
    OfferBlock,
)
