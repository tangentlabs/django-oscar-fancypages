from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation


from model_utils.managers import InheritanceManager

from fancypages.utils import get_container_names_from_template

Category = models.get_model('catalogue', 'Category')


#FIXME: this is a patch to bend the existing categories
# in Oscar to use the fancypages URLs without making any
# additional code or template changes necessary. This is
# not a good way of handling this. Oscar should be able
# to provide some sort of URL hook that allows for
# enabling, disabling and changing of named URLs
def get_absolute_url(self):
    return reverse(
        'fancypages:page-detail',
        args=(self.slug,)
    )
Category.get_absolute_url = get_absolute_url


class PageQuerySet(QuerySet):

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


class PageManager(models.Manager):
    def get_query_set(self):
        return PageQuerySet(self.model).order_by('category__path')


class PageType(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    slug = models.SlugField(_("Slug"), max_length=128)

    template_name = models.CharField(
        _("Template name"),
        max_length=255,
        default="fancypages/pages/page.html"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(PageType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'fancypages'


class Page(models.Model):
    category = models.OneToOneField(
        'catalogue.Category',
        verbose_name=_("Category"),
        related_name="page",
    )
    page_type = models.ForeignKey(
        'fancypages.PageType',
        verbose_name=_("Page type"),
        related_name="pages",
        null=True, blank=True,
    )

    keywords = models.CharField(
        _("Keywords"),
        max_length=255,
        null=True, blank=True
    )

    containers = generic.GenericRelation('fancypages.Container')

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

    objects = PageManager()

    @classmethod
    def add_root(cls, name, slug=None, page_type=None):
        category = Category.add_root(name=name, slug=slug)
        category.page.name = name
        if slug:
            category.page.slug = slug
        if not page_type:
            page_type, __ = PageType.objects.get_or_create(name='Default Template')
        category.page.page_type = page_type
        category.page.save()
        return category.page

    def add_child(self, name, slug=None, page_type=None):
        category = self.category.add_child(name=name, slug=slug)
        category.page.name = name
        if slug:
            category.page.slug = slug
        if not page_type:
            page_type, __ = PageType.objects.get_or_create(name='Default Template')
        category.page.page_type = page_type
        category.page.save()
        return category.page

    def delete(self, keep_category=False):
        super(Page, self).delete()
        if not keep_category:
            self.category.delete()

    def get_children(self):
        if self.category.is_leaf():
            return self.__class__.objects.none()
        path = self.category.path
        return self.__class__.objects.filter(
            category__depth=self.depth + 1,
            category__path__range=self.category._get_children_path_interval(path)
        )

    @property
    def title(self):
        return self.category.name

    @property
    def depth(self):
        return self.category.depth

    @property
    def numchild(self):
        return self.category.numchild

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

    @models.permalink
    def get_absolute_url(self):
        return ('fancypages:page-detail', (self.category.slug,), {})

    def __unicode__(self):
        return u"Page '%s'" % self.category.name

    def save(self, update_slugs=True, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)

        if not self.page_type:
            return

        existing_containers = [c.variable_name for c in self.containers.all()]
        for cname in get_container_names_from_template(self.page_type.template_name):
            if cname not in existing_containers:
                self.containers.create(page_object=self, variable_name=cname)

    class Meta:
        app_label = 'fancypages'


class Container(models.Model):
    template_name = 'fancypages/base/container.html'

    # this is the name of the variable used in the template tag
    # e.g. {% fancypages-container var-name %}
    title = models.CharField(max_length=100, null=True, blank=True)
    variable_name = models.SlugField(
        _("Variable name"),
        max_length=50,
        null=True, blank=True
    )

    # this makes the fancypages available to any type of object
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    page_object = generic.GenericForeignKey('content_type', 'object_id')

    def clean(self):
        if self.object_id and self.content_type:
            return

        from django.core.exceptions import ValidationError
        # Don't allow draft entries to have a pub_date.
        container_exists = Container.objects.filter(
            variable_name=self.variable_name,
            object_id=None,
            content_type=None,
        ).exists()
        if container_exists:
            raise ValidationError(
                "containter with name '%s' already exists" % self.variable_name
            )

    @classmethod
    def get_container_by_name(cls, name, obj=None):
        """
        Get container of *obj* with the specified variable *name*. It
        assumes that *obj* has a ``containers`` attribute and returns
        the container with *name* or ``None`` if it cannot be found.
        """
        if not obj:
            container, __ = cls.objects.get_or_create(
                content_type=None,
                variable_name=name,
                object_id=None,
            )
            return container

        object_type = ContentType.objects.get_for_model(obj)
        if object_type is None:
            return None

        ctn, __ = cls.objects.get_or_create(
            content_type=object_type,
            variable_name=name,
            object_id=obj.id
        )
        return ctn

    @classmethod
    def get_containers(cls, obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return cls.objects.filter(
            content_type__id=obj_type.id,
            object_id=obj.id
        )

    def save(self, *args, **kwargs):
        self.clean()
        if not self.variable_name:
            self.variable_name = "%s-%s" % (
                self._meta.module_name,
                Container.objects.count(),
            )
        return super(Container, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Container '%s' in '%s'" % (self.variable_name, self.content_type)

    class Meta:
        app_label = 'fancypages'
        unique_together = (('variable_name', 'content_type', 'object_id'),)


class Widget(models.Model):
    name = None
    code = None
    template_name = None
    renderer_class = None
    form_class = None

    container = models.ForeignKey(Container, verbose_name=_("Container"),
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
                widget_choices.append((
                    subclass.code,
                    subclass.name
                ))
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
        if _seen is None:
            _seen = set()
        try:
            subs = cls.__subclasses__()
        except TypeError:  # fails only when cls is type
            subs = cls.__subclasses__(cls)
        for sub in subs:
            if sub not in _seen:
                _seen.add(sub)
                yield sub
                for sub in sub.itersubclasses(_seen):
                    yield sub

    def get_renderer_class(self):
        from fancypages.renderers import WidgetRenderer
        return self.renderer_class or WidgetRenderer

    def save(self, **kwargs):
        if self.display_order is None:
            self.display_order = self.container.widgets.count()

        try:
            db_widget = Widget.objects.get(pk=self.pk)
        except Widget.DoesNotExist:
            db_widget = self

        db_container = db_widget.container
        db_display_order = db_widget.display_order

        super(Widget, self).save(**kwargs)

        if db_display_order != self.display_order \
           or self.container != db_container:
            self.fix_widget_positions(db_display_order, db_container)

    def fix_widget_positions(self, old_position, old_container):
        if self.container != old_container:
            for idx, widget in enumerate(old_container.widgets.all()):
                widget.display_order = idx
                widget.save()

        if self.display_order > old_position:
            widgets = self.container.widgets.filter(
                ~Q(id=self.id) &
                Q(display_order__lte=self.display_order)
            )
            for idx, widget in enumerate(widgets):
                widget.display_order = idx
                widget.save()

        else:
            widgets = self.container.widgets.filter(
                ~Q(id=self.id) &
                Q(display_order__gte=self.display_order)
            )
            for idx, widget in enumerate(widgets):
                widget.display_order = self.display_order + idx + 1
                widget.save()

    def __unicode__(self):
        return "Widget #%s" % self.id

    class Meta:
        ordering = ['display_order']
        app_label = 'fancypages'


class LayoutWidget(Widget):
    BOOTSTRAP_MAX_WIDTH = 12

    containers = GenericRelation('fancypages.Container')

    class Meta:
        abstract = True
        app_label = 'fancypages'


# this makes sure that when a new category is created without
# page that a page is created for the page
def create_page_for_category(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        Page.objects.get_or_create(category=instance)

post_save.connect(
    create_page_for_category,
    sender=models.get_model('catalogue', 'Category')
)
