from __future__ import absolute_import

from django.db import models
from django.conf import settings
from django.db import transaction, connection
from django.template.defaultfilters import slugify

from fancypages import manager
from fancypages import abstract_models

Category = models.get_model('catalogue', 'Category')


class FancyPage(Category, abstract_models.AbstractFancyPage):
    tb_table_name = Category._meta.db_table
    objects = manager.PageManager()

    @models.permalink
    def get_absolute_url(self):
        # make sure that the home view is actually redirecting to '/'
        # and not to '/home/'.
        if self.slug == slugify(getattr(settings, 'FP_HOMEPAGE_NAME')):
            return ('home', (), {})
        return ('fancypages:page-detail', (), {'slug': self.slug})

    def delete(self):
        "Removes a node and all it's descendants."
        self.__class__.objects.filter(id=self.id).delete()
        FancyPage.fix_tree()

    @classmethod
    def fix_tree(cls, destructive=False):
        """
        Solves some problems that can appear when transactions are not used and
        a piece of code breaks, leaving the tree in an inconsistent state.

        The problems this method solves are:

        1. Nodes with an incorrect ``depth`` or ``numchild`` values due to
        incorrect code and lack of database transactions.
        2. "Holes" in the tree. This is normal if you move/delete nodes a
        lot. Holes in a tree don't affect performance,
        3. Incorrect ordering of nodes when ``node_order_by`` is enabled.
        Ordering is enforced on *node insertion*, so if an attribute in
        ``node_order_by`` is modified after the node is inserted, the
        tree ordering will be inconsistent.

        :param destructive:

        A boolean value. If True, a more agressive fix_tree method will be
        attemped. If False (the default), it will use a safe (and fast!)
        fix approach, but it will only solve the ``depth`` and
        ``numchild`` nodes, it won't fix the tree holes or broken path
        ordering.

        .. warning::

        Currently what the ``destructive`` method does is:

        1. Backup the tree with :meth:`dump_data`
        2. Remove all nodes in the tree.
        3. Restore the tree with :meth:`load_data`

        So, even when the primary keys of your nodes will be preserved,
        this method isn't foreign-key friendly. That needs complex
        in-place tree reordering, not available at the moment (hint:
        patches are welcome).
        """
        if destructive:
            dump = cls.dump_bulk(None, True)
            cls.objects.all().delete()
            cls.load_bulk(dump, None, True)
        else:
            cursor = cls._get_database_cursor('write')

            # fix the depth field
            # we need the WHERE to speed up postgres
            sql = "UPDATE %s "\
                  "SET depth=LENGTH(path)/%%s "\
                  "WHERE depth!=LENGTH(path)/%%s" % (
                      connection.ops.quote_name(cls.tb_table_name), )
            vals = [cls.steplen, cls.steplen]
            cursor.execute(sql, vals)

            # fix the numchild field
            vals = ['_' * cls.steplen]
            # the cake and sql portability are a lie
            if cls.get_database_vendor('read') == 'mysql':
                sql = "SELECT tbn1.path, tbn1.numchild, ("\
                      "SELECT COUNT(1) "\
                      "FROM %(table)s AS tbn2 "\
                      "WHERE tbn2.path LIKE "\
                      "CONCAT(tbn1.path, %%s)) AS real_numchild "\
                      "FROM %(table)s AS tbn1 "\
                      "HAVING tbn1.numchild != real_numchild" % {
                          'table': connection.ops.quote_name(
                              cls.tb_table_name)}
            else:
                subquery = "(SELECT COUNT(1) FROM %(table)s AS tbn2"\
                           " WHERE tbn2.path LIKE tbn1.path||%%s)"
                sql = ("SELECT tbn1.path, tbn1.numchild, " + subquery +
                       " FROM %(table)s AS tbn1 WHERE tbn1.numchild != " +
                       subquery)
                sql = sql % {
                    'table': connection.ops.quote_name(cls.tb_table_name)}
                # we include the subquery twice
                vals *= 2
            cursor.execute(sql, vals)
            sql = "UPDATE %(table)s "\
                  "SET numchild=%%s "\
                  "WHERE path=%%s" % {
                      'table': connection.ops.quote_name(cls.tb_table_name)}
            for node_data in cursor.fetchall():
                vals = [node_data[2], node_data[0]]
                cursor.execute(sql, vals)

            transaction.commit_unless_managed()

    @classmethod
    def get_descendants_group_count(cls, parent=None):
        """
        Helper for a very common case: get a group of siblings and the number
        of *descendants* in every sibling.
        """
        #~
        # disclaimer: this is the FOURTH implementation I wrote for this
        # function. I really tried to make it return a queryset, but doing so
        # with a *single* query isn't trivial with Django's ORM.

        # ok, I DID manage to make Django's ORM return a queryset here,
        # defining two querysets, passing one subquery in the tables parameters
        # of .extra() of the second queryset, using the undocumented order_by
        # feature, and using a HORRIBLE hack to avoid django quoting the
        # subquery as a table, BUT (and there is always a but) the hack didn't
        # survive turning the QuerySet into a ValuesQuerySet, so I just used
        # good old SQL.
        # NOTE: in case there is interest, the hack to avoid django quoting the
        # subquery as a table, was adding the subquery to the alias cache of
        # the queryset's query object:
        #
        # qset.query.quote_cache[subquery] = subquery
        #
        # If there is a better way to do this in an UNMODIFIED django 1.0, let
        # me know.
        #~

        if parent:
            depth = parent.depth + 1
            params = cls._get_children_path_interval(parent.path)
            extrand = 'AND path BETWEEN %s AND %s'
        else:
            depth = 1
            params = []
            extrand = ''

        sql = 'SELECT * FROM %(table)s AS t1 INNER JOIN '\
              ' (SELECT '\
              ' SUBSTR(path, 1, %(subpathlen)s) AS subpath, '\
              ' COUNT(1)-1 AS count '\
              ' FROM %(table)s '\
              ' WHERE depth >= %(depth)s %(extrand)s'\
              ' GROUP BY subpath) AS t2 '\
              ' ON t1.path=t2.subpath '\
              ' ORDER BY t1.path' % {
                  'table': connection.ops.quote_name(cls.tb_table_name),
                  'subpathlen': depth * cls.steplen,
                  'depth': depth,
                  'extrand': extrand}
        cursor = cls._get_database_cursor('write')
        cursor.execute(sql, params)

        ret = []
        field_names = [field[0] for field in cursor.description]
        for node_data in cursor.fetchall():
            node = cls(**dict(zip(field_names, node_data[:-2])))
            node.descendants_count = node_data[-1]
            ret.append(node)
        transaction.commit_unless_managed()
        return ret

    @classmethod
    def _get_sql_newpath_in_branches(cls, oldpath, newpath):
        """
        :returns" The sql needed to move a branch to another position.

        .. note::

        The generated sql will only update the depth values if needed.

        """
        vendor = cls.get_database_vendor('write')
        sql1 = "UPDATE %s SET" % (
            connection.ops.quote_name(cls.tb_table_name), )

        # <3 "standard" sql
        if vendor == 'sqlite':
            # I know that the third argument in SUBSTR (LENGTH(path)) is
            # awful, but sqlite fails without it:
            # OperationalError: wrong number of arguments to function substr()
            # even when the documentation says that 2 arguments are valid:
            # http://www.sqlite.org/lang_corefunc.html
            sqlpath = "%s||SUBSTR(path, %s, LENGTH(path))"
        elif vendor == 'mysql':
            # hooray for mysql ignoring standards in their default
            # configuration!
            # to make || work as it should, enable ansi mode
            # http://dev.mysql.com/doc/refman/5.0/en/ansi-mode.html
            sqlpath = "CONCAT(%s, SUBSTR(path, %s))"
        else:
            sqlpath = "%s||SUBSTR(path, %s)"

        sql2 = ["path=%s" % (sqlpath, )]
        vals = [newpath, len(oldpath) + 1]
        if len(oldpath) != len(newpath) and vendor != 'mysql':
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
        sql = "UPDATE %s SET depth=LENGTH(path)/%%s"\
              " WHERE path LIKE %%s" % (
                  connection.ops.quote_name(cls.tb_table_name), )
        vals = [cls.steplen, path + '%']
        return sql, vals

    @classmethod
    def _get_sql_update_numchild(cls, path, incdec='inc'):
        """:returns: The sql needed the numchild value of a node"""
        sql = "UPDATE %s SET numchild=numchild%s1"\
              " WHERE path=%%s" % (
                  connection.ops.quote_name(cls.tb_table_name),
                  {'inc': '+', 'dec': '-'}[incdec])
        vals = [path]
        return sql, vals


# We have to import all models from django-fancypages AFTER re-defining
# FancyPage because otherwise we'll import it FancyPage first and will use
# the wrong one.
from fancypages.models import (
    FancyPage,
    PageGroup,
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
    VideoBlock,
    TwitterBlock
)


from .product import (
    SingleProductBlock,
    HandPickedProductsPromotionBlock,
    AutomaticProductsPromotionBlock,
    PrimaryNavigationBlock,
    OfferBlock,
)
