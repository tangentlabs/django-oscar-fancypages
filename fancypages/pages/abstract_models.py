from django.db import models
from django.utils import timezone
from django.template import loader
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import PassThroughManager

from fancypages.templatetags.fancypages_tags import FancyContainerNode


class PageQuerySet(models.query.QuerySet):

    def visible(self):
        now = timezone.now()
        return self.filter(
            status=AbstractPage.PUBLISHED,
            is_visible=True,
        ).filter(
            models.Q(date_visible_start=None) |
            models.Q(date_visible_start__lt=now),
            models.Q(date_visible_end=None) |
            models.Q(date_visible_end__gt=now)
        )

# TODO the AbstractPage should use django-treebeard in the future
# to make sure that the hierarchy is handled properly. This will
# also simplify moving pages around in the hierarchy
class AbstractPage(models.Model):
    template_name = None

    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100)

    parent = models.ForeignKey('self', verbose_name=_(u"Parent page"))

    # this is the *cached* relative URL for this page taking parent 
    # slugs into account. This is updated on save
    relative_url = models.CharField(max_length=500)

    PUBLISHED, DRAFT, ARCHIVED = (u'published', u'draft', u'archived')
    STATUS_CHOICES = (
        (PUBLISHED, _("Published")),
        (DRAFT, _("Draft")),
        (ARCHIVED, _("Archived")),
    )
    status = models.CharField(_(u"Status"), max_length=15, choices=STATUS_CHOICES)

    date_visible_start = models.DateTimeField(_("Visible from"), null=True, blank=True)
    date_visible_end = models.DateTimeField(_("Visible until"), null=True, blank=True)

    is_visible = models.BooleanField(_("Is visible"), default=True)

    objects = PassThroughManager.for_queryset_class(PageQuerySet)()

    def get_container_names(self):
        if not self.template_name:
            return []

        container_names = []
        for node in loader.get_template(self.template_name):
            container_nodes = node.get_nodes_by_type(FancyContainerNode)

            for cnode in container_nodes:
                var_name = cnode.container_name.var
                if var_name in container_names:
                    raise ImproperlyConfigured(
                        "duplicate container name '%s' in template '%s'",
                        var_name,
                        self.template_name
                    )
                    continue
                container_names.append(var_name)

        return container_names

    class Meta:
        abstract = True


class AbstractArticlePage(AbstractPage):
    template_name = "fancypages/pages/article_page.html"

    class Meta:
        abstract = True


class AbstractContainer(models.Model):
    # this is the name of the variable used in the template tag
    # e.g. {% fancypages-container var-name %}
    variable_name = models.SlugField(_("Variable name"), max_length=50)
    #page = models.ForeignKey('pages.

    class Meta:
        abstract = True
