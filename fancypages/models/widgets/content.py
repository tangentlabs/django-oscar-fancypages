import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fancypages.models.base import Widget
from fancypages.assets.fields import AssetKey
from fancypages.models.mixins import ImageMetadataMixin

ImageAsset = models.get_model('assets', 'ImageAsset')


class TextWidget(Widget):
    name = _("Text")
    code = 'text'
    group = _("Content")
    template_name = "fancypages/widgets/textwidget.html"

    text = models.TextField(_("Text"), default="Your text goes here.")

    def __unicode__(self):
        return self.text[:20]

    class Meta:
        app_label = 'fancypages'


class TitleTextWidget(Widget):
    name = _("Title and text")
    code = 'title-text'
    group = _("Content")
    template_name = "fancypages/widgets/titletextwidget.html"

    title = models.CharField(_("Title"), max_length=100,
                             default="Your title goes here.")
    text = models.TextField(_("Text"), default="Your text goes here.")

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'fancypages'


class ImageWidget(ImageMetadataMixin, Widget):
    name = _("Image")
    code = 'image'
    group = _("Content")
    template_name = "fancypages/widgets/imagewidget.html"

    image_asset = AssetKey('assets.ImageAsset', verbose_name=_("Image asset"),
                           related_name="image_widgets", blank=True, null=True)

    def __unicode__(self):
        return u"Image #%s" % self.id

    class Meta:
        app_label = 'fancypages'


class ImageAndTextWidget(ImageMetadataMixin, Widget):
    name = _("Image and text")
    code = 'image-text'
    group = _("Content")
    template_name = "fancypages/widgets/imageandtextwidget.html"

    image_asset = AssetKey(
        'assets.ImageAsset',
        verbose_name=_("Image asset"),
        related_name="image_text_widgets",
        blank=True,
        null=True,
    )

    text = models.CharField(
        _("Text"),
        max_length=2000,
        default="Your text goes here."
    )

    def __unicode__(self):
        return u"Image with text #%s" % self.id

    class Meta:
        app_label = 'fancypages'


class CarouselWidget(Widget):
    name = _("Image carousel")
    code = 'carousel'
    group = _("Content")
    num_images = 10
    image_field_name = "image_%d"
    link_field_name = "link_url_%d"
    template_name = "fancypages/widgets/carouselwidget.html"

    def get_images_and_links(self):
        results = {}
        query = models.Q()
        for idx in range(1, self.num_images+1):
            image_id = getattr(self, "%s_id" % (self.image_field_name % idx))
            link_field_name = self.link_field_name % idx
            if image_id:
                results[image_id] = {'link': getattr(self, link_field_name, None)}
                query.add(models.Q(id=image_id), models.Q.OR)
        if not query:
            return {}
        for image in ImageAsset.objects.filter(query):
            results[image.id]['image'] = image
        return results

    def __unicode__(self):
        return u"Carousel #%s" % self.id

    class Meta:
        app_label = 'fancypages'


# generate the image field for the CarouselWidget dynamically
# because I am lazy ;)
for idx in range(1, CarouselWidget.num_images + 1):
    CarouselWidget.add_to_class(
        CarouselWidget.image_field_name % idx,
        AssetKey(
            'assets.ImageAsset',
            verbose_name=_("Image %d" % idx),
            related_name="+",
            blank=True,
            null=True,
        )
    )
    CarouselWidget.add_to_class(
        CarouselWidget.link_field_name % idx,
        models.CharField(
            _("Link URL %d" % idx),
            max_length=500,
            blank=True, null=True
        )
    )


class PageNavigationWidget(Widget):
    name = _("Page Navigation")
    code = 'page-navigation'
    group = _("Content")
    template_name = "fancypages/widgets/pagenavigationwidget.html"

    def __unicode__(self):
        return u'Page Navigation'

    class Meta:
        app_label = 'fancypages'


class PrimaryNavigationWidget(Widget):
    name = _("Primary Navigation")
    code = 'primary-navigation'
    group = _("Content")
    template_name = "fancypages/widgets/primarynavigationwidget.html"

    def __unicode__(self):
        return u'Primary Navigation'

    class Meta:
        app_label = 'fancypages'
