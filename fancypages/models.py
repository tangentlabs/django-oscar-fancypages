from django.db import models

from django.utils.translation import ugettext_lazy as _


class PageLayout(models.Model):
    name = models.CharField(_("Name"), max_length=255)


class LayoutSection(models.Model):
    layout = models.ForeignKey("fancypages.PageLayout", related_name="sections",
                               verbose_name=_("Layout"))
    slug = models.SlugField(help_text=_("This is the name use in the template "
                                        "for the corresponding block template tag"))


class Page(models.Model):
    # allow for hierarchical structure of pages
    parent = models.ForeignKey('self', related_name="children",
                               verbose_name=_("Parent page"))

    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)

    def __unicode__(self):
        if self.parent:
            return "%s - %s" % (self.parent, self.title)
        return self.title


class BaseContent(models.Model):
    page = models.ForeignKey("fancypages.Page", related_name="content_elements",
                             verbose_name=_("Page"))
    section = models.ForeignKey("fancypages.LayoutSection", related_name="content",
                                verbose_name=_("Section"))

    class Meta:
        abstract = True


class TitleText(BaseContent):
    title  = models.CharField(_("Title"), max_length=300)
    text = models.CharField(_("Text"), max_length=2000)


class TextImage(BaseContent):
    text = models.CharField(_("Text"), max_length=2000)
    image = models.ImageField(_("Image"), upload_to="fancypages/content/images")
