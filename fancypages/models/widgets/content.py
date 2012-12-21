import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from fancypages.models.base import Widget, ImageMetadataMixin


class TextWidget(Widget):
    name = _("Text")
    code = 'text'
    template_name = "fancypages/widgets/textwidget.html"

    text = models.TextField(_("Text"), default="Your text goes here.")

    def __unicode__(self):
        return self.text[:20]

    class Meta:
        app_label = 'fancypages'


class TitleTextWidget(Widget):
    name = _("Title and text")
    code = 'title-text'
    template_name = "fancypages/widgets/titletextwidget.html"

    title = models.CharField(_("Title"), max_length=100,
                             default="Your title goes here.")
    text = models.TextField(_("Text"), default="Your text goes here.")

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'fancypages'


class ImageWidget(Widget, ImageMetadataMixin):
    name = _("Image")
    code = 'image'
    template_name = "fancypages/widgets/imagewidget.html"

    image_asset = models.ForeignKey('assets.ImageAsset', verbose_name=_("Image asset"),
                                    related_name="image_widgets", blank=True, null=True)

    def __unicode__(self):
        if self.image_asset:
            return u"Image '%s'" % os.path.basename(self.image_asset.image.path)
        return u"Image #%s" % self.id

    class Meta:
        app_label = 'fancypages'


class ImageAndTextWidget(Widget, ImageMetadataMixin):
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

    class Meta:
        app_label = 'fancypages'
