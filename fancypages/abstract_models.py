from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.template import loader, Context, RequestContext
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import PassThroughManager, InheritanceQuerySet

from fancypages.templatetags.fancypages_tags import FancyContainerNode


class AbstractPageType(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    code = models.SlugField(_("Code"), max_length=100, unique=True)

    template_name = models.CharField(_("Template name"), max_length=500)

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
                container_names.append(var_name)
        return container_names

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)
        super(AbstractPageType, self).save(*args, **kwargs)

    def __unicode__(self):
        return "Page type: %s" % self.name

    class Meta:
        abstract = True


class PageQuerySet(InheritanceQuerySet):

    def visible(self):
        now = timezone.now()
        return self.filter(
            status=AbstractPage.PUBLISHED,
            is_active=True,
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
    title = models.CharField(_("Title"), max_length=100)
    code = models.SlugField(_("Code"), max_length=100, unique=True)

    page_type = models.ForeignKey('fancypages.PageType',
                                  verbose_name=_("Page type"),
                                  related_name="pages")

    parent = models.ForeignKey('self', verbose_name=_(u"Parent page"),
                               null=True, blank=True, 
                               related_name="children")

    # this is the *cached* relative URL for this page taking parent
    # slugs into account. This is updated on save
    relative_url = models.CharField(max_length=500, null=True, blank=True)

    PUBLISHED, DRAFT, ARCHIVED = (u'published', u'draft', u'archived')
    STATUS_CHOICES = (
        (PUBLISHED, _("Published")),
        (DRAFT, _("Draft")),
        (ARCHIVED, _("Archived")),
    )
    status = models.CharField(_(u"Status"), max_length=15, choices=STATUS_CHOICES,
                              default=DRAFT)

    date_visible_start = models.DateTimeField(_("Visible from"), null=True, blank=True)
    date_visible_end = models.DateTimeField(_("Visible until"), null=True, blank=True)

    # overrides the visibility date range when set to false making the
    # page invisible
    is_active = models.BooleanField(_("Is active"), default=True)

    objects = PassThroughManager.for_queryset_class(PageQuerySet)()

    @property
    def is_visible(self):
        if not self.is_active:
            return False

        if self.status != AbstractPage.PUBLISHED:
            return False

        now = timezone.now()
        if self.date_visible_start \
           and self.date_visible_start > now:
            return False

        if self.date_visible_end \
           and self.date_visible_end < now:
            return False

        return True

    def create_container(self, name):
        if self.containers.filter(variable_name=name).count():
            return
        self.containers.create(variable_name=name)

    def initialise_containers(self):
        for name in self.get_container_names():
            self.containers.create(variable_name=name)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.title)
        super(AbstractPage, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s with title '%s'" % (self.type.name, self.title)

    class Meta:
        abstract = True


class AbstractContainer(models.Model):
    # this is the name of the variable used in the template tag
    # e.g. {% fancypages-container var-name %}
    variable_name = models.SlugField(_("Variable name"), max_length=50)

    page = models.ForeignKey('fancypages.Page', verbose_name=_("Page"),
                             related_name='containers')

    class Meta:
        abstract = True


class AbstractWidget(models.Model):
    name = None
    template_name = None
    context_object_name = 'object'

    container = models.ForeignKey('fancypages.Container',
                                  verbose_name=_("Container"),
                                  related_name="widgets")

    def render(self, request=None):
        if not self.template_name:
            raise ImproperlyConfigured(
                "a template name is required for a widget to be rendered"
            )

        tmpl = loader.get_template(self.template_name)
        if request:
            ctx = RequestContext(request)
        else:
            ctx = Context()
        ctx[self.context_object_name] = self
        return tmpl.render(ctx)

    class Meta:
        abstract = True


class AbstractTextWidget(models.Model):
    name = _("Text widget")
    template_name = "fancypages/widgets/text_widget.html"

    text = models.CharField(_("Text"), max_length=2000)

    class Meta:
        abstract = True


class AbstractTitleTextWidget(models.Model):
    name = _("Title and text widget")
    template_name = "fancypages/widgets/title_text_widget.html"

    title = models.CharField(_("Title"), max_length=100)
    text = models.CharField(_("Text"), max_length=2000)

    class Meta:
        abstract = True


class AbstractImageWidget(models.Model):
    name = _("Image widget")
    template_name = "fancypages/widgets/image_widget.html"

    image = models.ImageField(_("Image"), upload_to="fancypages/%y/%m/")
    caption = models.CharField(_("Caption"), max_length=200,
                               null=True, blank=True)

    class Meta:
        abstract = True
