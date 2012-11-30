import os

from django.db import models
from django.utils import timezone
from django.forms import ValidationError
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.template import loader, RequestContext, Context

from model_utils.managers import InheritanceManager
from treebeard.mp_tree import MP_Node, MP_NodeQuerySet

from fancypages.utils import get_container_names_from_template


class PageQuerySet(MP_NodeQuerySet):

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
    """
    This manager is required to provide access to ``treebeard``'s custom
    manager and queryset. Otherwise it breaks the category handling.
    """
    def get_query_set(self):
        return PageQuerySet(self.model).order_by('path')


class Page(MP_Node):
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(_("Code"), max_length=100, unique=True)

    template_name = models.CharField(_("Template name"), max_length=255,
                                     default="fancypages/pages/page.html")

    description = models.TextField(_("Description"), null=True, blank=True,
                                   default=None)
    keywords = models.CharField(_("Keywords"), max_length=255, null=True,
                                blank=True)

    # this is the *cached* relative URL for this page taking parent
    # slugs into account. This is updated on save
    relative_url = models.CharField(max_length=500, null=True, blank=True)

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

    _slug_separator = '/'

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
        return ('fancypages:page-detail', (), {
                'slug': self.slug})

    def __unicode__(self):
        return u"Page '%s'" % self.title

    def save(self, update_slugs=True, *args, **kwargs):
        if update_slugs:
            parent = self.get_parent()
            slug = slugify(self.title)
            if parent:
                self.slug = '%s%s%s' % (
                    parent.slug,
                    self._slug_separator,
                    slug
                )
            else:
                self.slug = slug

        # Enforce slug uniqueness here as MySQL can't handle a unique index on
        # the slug field
        try:
            match = self.__class__.objects.get(slug=self.slug)
        except self.__class__.DoesNotExist:
            pass
        else:
            if match.id != self.id:
                raise ValidationError(
                    _("A category with slug '%(slug)s' already exists") % {
                        'slug': self.slug
                    })

        super(Page, self).save(*args, **kwargs)

        existing_containers = [c.variable_name for c in self.containers.all()]
        for cname in get_container_names_from_template(self.template_name):
            if cname not in existing_containers:
                self.containers.create(page_object=self, variable_name=cname)

    def move(self, target, pos=None):
        super(Page, self).move(target, pos)

        reloaded_self = self.__class__.objects.get(pk=self.pk)
        subtree = self.__class__.get_tree(parent=reloaded_self)
        if subtree:
            slug_parts = []
            curr_depth = 0
            parent = reloaded_self.get_parent()
            if parent:
                slug_parts = [parent.slug]
                curr_depth = parent.depth
            self.__class__.update_subtree_properties(
                list(subtree),
                slug_parts,
                curr_depth=curr_depth
            )

    @classmethod
    def update_subtree_properties(cls, nodes, slug_parts, curr_depth):
        """
        Update slugs and full_names of children in a subtree.
        Assumes nodes were originally in DFS order.
        """
        if nodes == []:
            return

        node = nodes[0]
        if node.depth > curr_depth:
            slug = slugify(node.title)
            slug_parts.append(slug)

            node.slug = cls._slug_separator.join(slug_parts)
            node.save(update_slugs=False)
            curr_depth += 1
            nodes = nodes[1:]

        else:
            slug_parts = slug_parts[:-1]
            curr_depth -= 1

        cls.update_subtree_properties(
            nodes,
            slug_parts,
            curr_depth
        )


class Container(models.Model):
    template_name = 'fancypages/base/container.html'

    # this is the name of the variable used in the template tag
    # e.g. {% fancypages-container var-name %}
    title = models.CharField(max_length=100, null=True, blank=True)
    variable_name = models.SlugField(_("Variable name"), max_length=50,
                                     null=True, blank=True)

    # this makes the fancypages available to any type of object
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    page_object = generic.GenericForeignKey('content_type', 'object_id')

    def render(self, request=None, **kwargs):
        """
        Render the container and all its contained widgets.
        """
        ordered_widgets = self.widgets.select_subclasses()

        tmpl = loader.get_template(self.template_name)

        if request:
            ctx = RequestContext(request)
        else:
            ctx = Context()

        ctx['container'] = self
        ctx['rendered_widgets'] = []

        for widget in ordered_widgets:
            try:
                rendered_widget = widget.render(request, **kwargs)
            except ImproperlyConfigured:
                continue

            ctx['rendered_widgets'].append((widget.id, rendered_widget))

        ctx.update(kwargs)
        return tmpl.render(ctx)

    @classmethod
    def get_container_by_name(cls, obj, name):
        """
        Get container of *obj* with the specified variable *name*. It
        assumes that *obj* has a ``containers`` attribute and returns
        the container with *name* or ``None`` if it cannot be found.
        """
        obj_type = ContentType.objects.get_for_model(obj)
        if obj_type is None:
            return None

        ctn, __ = cls.objects.get_or_create(content_type=obj_type,
                                            variable_name=name,
                                            object_id=obj.id)
        return ctn

    @classmethod
    def get_containers(cls, obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return cls.objects.filter(content_type__id=obj_type.id)

    def __unicode__(self):
        return u"Container '%s' in '%s'" % (self.variable_name, self.content_type)


class OrderedContainer(Container):
    display_order = models.PositiveIntegerField()

    def __unicode__(self):
        return u"Container #%d '%s' in '%s'" % (
            self.display_order,
            self.variable_name,
            self.content_type
        )


class Widget(models.Model):
    name = None
    code = None
    template_name = None
    context_object_name = 'object'

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

    def render(self, request=None, **kwargs):
        if not self.template_name:
            raise ImproperlyConfigured(
                "a template name is required for a widget to be rendered"
            )


        if request:
            ctx = RequestContext(request)
        else:
            ctx = Context()

        ctx[self.context_object_name] = self
        ctx.update(kwargs)

        tmpl = loader.get_template(self.template_name)
        return tmpl.render(ctx)

    def save(self, **kwargs):
        if self.display_order is None:
            self.display_order = self.container.widgets.count()
        super(Widget, self).save(**kwargs)

    def __unicode__(self):
        return "Widget #%s" % self.id

    class Meta:
        ordering = ['display_order']


#class ContainerWidget(Widget):
#    """
#    A widget that provides another container instead of an actual
#    widget. It provides a way of nesting containers.
#    """
#    class Meta:
#        abstract = True


class TextWidget(Widget):
    name = _("Text")
    code = 'text'
    template_name = "fancypages/widgets/textwidget.html"

    text = models.CharField(_("Text"), max_length=2000,
                            default="Your text goes here.")

    def __unicode__(self):
        return self.text[:20]


class TitleTextWidget(Widget):
    name = _("Title and text")
    code = 'title-text'
    template_name = "fancypages/widgets/titletextwidget.html"

    title = models.CharField(_("Title"), max_length=100,
                             default="Your title goes here.")
    text = models.CharField(_("Text"), max_length=2000,
                            default="Your text goes here.")

    def __unicode__(self):
        return self.title


class ImageMetaMixin(models.Model):
    """
    Mixin for meta data for image widgets
    """
    title = models.CharField(_("Image title"), max_length=100, blank=True, null=True)
    alt_text = models.CharField(_("Alternative text"), max_length=100, blank=True, null=True)
    link = models.CharField(_("Link URL"), max_length=500, blank=True, null=True)

    class Meta:
        abstract = True


class ImageWidget(Widget, ImageMetaMixin):
    name = _("Image")
    code = 'image'
    template_name = "fancypages/widgets/imagewidget.html"

    image_asset = models.ForeignKey('assets.ImageAsset', verbose_name=_("Image asset"),
                                    related_name="image_widgets", blank=True, null=True)

    def __unicode__(self):
        if self.image_asset:
            return u"Image '%s'" % os.path.basename(self.image_asset.image.path)
        return u"Image #%s" % self.id


class SingleProductWidget(Widget):
    name = _("Single Product")
    code = 'single-product'
    template_name = "fancypages/widgets/productwidget.html"

    product = models.ForeignKey(
        'catalogue.Product',
        verbose_name=_("Single Product"), null=True, blank=False)

    def __unicode__(self):
        if self.product:
            return u"Product '%s'" % self.product.upc
        return u"Product '%s'" % self.id


class HandPickedProductsPromotionWidget(Widget):
    name = _("Hand Picked Products Promotion")
    code = 'promotion-hand-picked-products'
    template_name = "fancypages/widgets/promotionwidget.html"

    promotion = models.ForeignKey(
        'promotions.HandPickedProductList',
        verbose_name=_("Hand Picked Products Promotion"), null=True, blank=False)

    def __unicode__(self):
        if self.promotion:
            return u"Promotion '%s'" % self.promotion.pk
        return u"Promotion '%s'" % self.id


class AutomaticProductsPromotionWidget(Widget):
    name = _("Automatic Products Promotion")
    code = 'promotion-ordered-products'
    template_name = "fancypages/widgets/promotionwidget.html"

    promotion = models.ForeignKey(
        'promotions.AutomaticProductList',
        verbose_name=_("Automatic Products Promotion"), null=True, blank=False)

    def __unicode__(self):
        if self.promotion:
            return u"Promotion '%s'" % self.promotion.pk
        return u"Promotion '%s'" % self.id


class OfferWidget(Widget):
    name = _("Offer Products")
    code = 'products-range'
    template_name = "fancypages/widgets/offerwidget.html"

    offer = models.ForeignKey(
        'offer.ConditionalOffer',
        verbose_name=_("Offer"), null=True, blank=False)

    @property
    def products(self):
        range = self.offer.condition.range
        if range.includes_all_products:
            return Product.browsable.filter(is_discountable=True)
        return range.included_products.filter(is_discountable=True)

    def __unicode__(self):
        if self.offer:
            return u"Offer '%s'" % self.offer.pk
        return u"Offer '%s'" % self.id


class ImageAndTextWidget(Widget, ImageMetaMixin):
    name = _("Image and text")
    code = 'image-text'
    template_name = "fancypages/widgets/imageandtextwidget.html"

    image_asset = models.ForeignKey('assets.ImageAsset', verbose_name=_("Image asset"),
                                    related_name="image_text_widgets", blank=True, null=True)

    text = models.CharField(_("Text"), max_length=2000,
                                   default="Your text goes here.")

    def __unicode__(self):
        if self.image_asset:
            return u"Image with text '%s'" % os.path.basename(self.image_asset.image.path)
        return u"Image with text #%s" % self.id


class TabWidget(Widget):
    name = _("Tabbed block")
    code = 'tabbed-block'
    context_object_name = "widget"
    template_name = "fancypages/widgets/tabbedblockwidget.html"

    tabs = generic.GenericRelation('fancypages.OrderedContainer')

    def save(self, *args, **kwargs):
        super(TabWidget, self).save(*args, **kwargs)
        if not self.tabs.count():
            OrderedContainer.objects.create(page_object=self, display_order=0,
                                            title=_("New Tab"))


class VideoWidget(Widget):
    name = _("Video")
    code = 'video'
    template_name = "fancypages/widgets/video.html"

    SOURCE_YOUTUBE = 'youtube'
    SOURCES = (
        (SOURCE_YOUTUBE, _('YouTube video')),
    )

    source = models.CharField(_('Video Type'), choices=SOURCES, max_length=50)
    video_code = models.CharField(_('Video Code'), max_length=50)

    def __unicode__(self):
        if self.source:
            return "Video '%s'" % self.video_code
        return "Video #%s" % self.id


class TwitterWidget(Widget):
    name = _("Twitter")
    code = 'twitter'
    template_name = "fancypages/widgets/twitter.html"

    username = models.CharField(_('Twitter username'), max_length=50)
    max_tweets = models.PositiveIntegerField(_('Maximum tweets'), default=5)

    def __unicode__(self):
        if self.username:
            return u"Twitter user '@%s'" % self.username
        return u"Twitter: %s" % self.id


class LayoutWidget(Widget):
    BOOTSTRAP_MAX_WIDTH = 12

    containers = generic.GenericRelation('fancypages.Container')
    class Meta:
        abstract = True


class TwoColumnLayoutWidget(LayoutWidget):
    name = _("Two column layout")
    code = 'two-column-layout'
    template_name = "fancypages/widgets/two_column_layout.html"

    LEFT_WIDTH_CHOICES = [(x, x) for x in range(1, 12)]
    left_width = models.PositiveIntegerField(_("Left Width"), max_length=3,
                                             choices=LEFT_WIDTH_CHOICES, default=6)

    @property
    def left_span(self):
        """ Returns the bootstrap span class for the left container. """
        return u'span%d' % self.left_width

    @property
    def right_span(self):
        """ Returns the bootstrap span class for the left container. """
        return u'span%d' % (self.BOOTSTRAP_MAX_WIDTH - self.left_width)


class ThreeColumnLayoutWidget(LayoutWidget):
    name = _("Three column layout")
    code = 'three-column-layout'
    template_name = "fancypages/widgets/three_column_layout.html"


class FourColumnLayoutWidget(LayoutWidget):
    name = _("Four column layout")
    code = 'four-column-layout'
    template_name = "fancypages/widgets/four_column_layout.html"
