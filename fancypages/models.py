import os

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.template import loader, Context, RequestContext

from model_utils.managers import (PassThroughManager,
                                  InheritanceQuerySet,
                                  InheritanceManager)


class PageTemplate(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    description = models.CharField(_("Description"), max_length=500)
    icon = models.ImageField(_("Icon"), upload_to="fancypages/icons",
                             null=True, blank=True)

    template_name = models.CharField(_("Template name"), max_length=255)

    def __unicode__(self):
        return self.title


class PageType(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    code = models.SlugField(_("Code"), max_length=100, unique=True)

    template =  models.ForeignKey("fancypages.PageTemplate",
                                  verbose_name=_("Page template"),
                                  related_name="page_types")

    def get_container_names(self):
        if not self.template.template_name:
            return []

        # FIXME: This import should be at the top of the file but causes
        # a problem due to circluar import. This needs a closer look to fix it
        # properly
        from fancypages.templatetags import fancypages_tags
        container_names = []
        for node in loader.get_template(self.template.template_name):
            container_nodes = node.get_nodes_by_type(fancypages_tags.FancyContainerNode)

            for cnode in container_nodes:
                var_name = cnode.container_name.var
                if var_name in container_names:
                    raise ImproperlyConfigured(
                        "duplicate container name '%s' in template '%s'",
                        var_name,
                        self.template.template_name
                    )
                container_names.append(var_name)
        return container_names

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)
        super(PageType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class PageQuerySet(InheritanceQuerySet):

    def visible(self):
        now = timezone.now()
        return self.filter(
            status=Page.PUBLISHED,
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
class Page(models.Model):
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

        if self.status != Page.PUBLISHED:
            return False

        now = timezone.now()
        if self.date_visible_start \
           and self.date_visible_start > now:
            return False

        if self.date_visible_end \
           and self.date_visible_end < now:
            return False

        return True

    def get_container_from_name(self, name):
        try:
            return self.containers.get(variable_name=name)
        except models.get_model('fancypages', 'Container').DoesNotExist:
            return None

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

        super(Page, self).save(*args, **kwargs)

        existing_containers = [c.variable_name for c in self.containers.all()]
        for cname in self.page_type.get_container_names():
            if cname not in existing_containers:
                self.containers.create(
                    page=self,
                    variable_name=cname,
                )

    def __unicode__(self):
        return u"%s with title '%s'" % (self.page_type.name, self.title)


class Container(models.Model):
    template_name = 'fancypages/container.html'
    # this is the name of the variable used in the template tag
    # e.g. {% fancypages-container var-name %}
    variable_name = models.SlugField(_("Variable name"), max_length=50)

    page = models.ForeignKey('fancypages.Page', verbose_name=_("Page"),
                             related_name='containers')

    def render(self, request=None, **kwargs):
        ordered_widgets = self.widgets.select_subclasses()

        tmpl = loader.get_template(self.template_name)

        if request:
            ctx = RequestContext(request)
        else:
            ctx = Context()

        ctx['container_name'] = self.variable_name
        ctx['rendered_widgets'] = []
        for widget in ordered_widgets:
            ctx['rendered_widgets'].append(
                (widget.id, widget.render(request, **kwargs))
            )

        ctx.update(kwargs)
        return tmpl.render(ctx)

    def __unicode__(self):
        return u"Container '%s' in '%s'" % (self.variable_name, self.page.title)


class Widget(models.Model):
    name = None
    code = None
    template_name = None
    context_object_name = 'object'

    container = models.ForeignKey('fancypages.Container', verbose_name=_("Container"),
                                  related_name="widgets")

    display_order = models.PositiveIntegerField()

    objects = InheritanceManager()

    @classmethod
    def get_available_widgets(cls):
        widget_choices = []
        for subclass in cls.itersubclasses():
            if not subclass._meta.abstract:
                if not subclass.name:
                    raise ImproperlyConfigured(
                        "widget subclasses have to provide 'name' attributes"
                    )
                widget_choices.append((subclass.code, subclass.name))
        return widget_choices

    @classmethod
    def itersubclasses(cls, _seen=None):
        """
        I have taken this method from:

        http://code.activestate.com/recipes/576949-find-all-subclasses-of-a-given-class/

        so that I don't have to do this all myself :)
        """
        if not isinstance(cls, type):
            raise TypeError('itersubclasses must be called with '
                            'new-style classes, not %.100r' % cls)
        if _seen is None: _seen = set()
        try:
            subs = cls.__subclasses__()
        except TypeError: # fails only when cls is type
            subs = cls.__subclasses__(cls)
        for sub in subs:
            if sub not in _seen:
                _seen.add(sub)
                yield sub
                for sub in sub.itersubclasses(_seen):
                    yield sub

    def render(self, request=None, **kwargs):
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
        ctx.update(kwargs)
        return tmpl.render(ctx)

    def save(self, **kwargs):
        if self.display_order is None:
            self.display_order = self.container.widgets.count()
        super(Widget, self).save(**kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['display_order']


class TextWidget(Widget):
    name = _("Text widget")
    code = 'text'
    template_name = "fancypages/widgets/text_widget.html"

    text = models.CharField(_("Text"), max_length=2000)

    def __unicode__(self):
        return self.text[:20]


class TitleTextWidget(Widget):
    name = _("Title and text widget")
    code = 'title-text'
    template_name = "fancypages/widgets/title_text_widget.html"

    title = models.CharField(_("Title"), max_length=100)
    text = models.CharField(_("Text"), max_length=2000)

    def __unicode__(self):
        return self.title


class ImageWidget(Widget):
    name = _("Image widget")
    code = 'image'
    template_name = "fancypages/widgets/image_widget.html"

    image = models.ImageField(_("Image"), upload_to="fancypages/%y/%m/")
    caption = models.CharField(_("Caption"), max_length=200,
                               null=True, blank=True)

    def __unicode__(self):
        return u"Image '%s'" % os.path.basename(self.image.path)
