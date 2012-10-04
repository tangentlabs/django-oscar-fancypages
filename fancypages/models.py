import os

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.template import loader, Context, RequestContext

from model_utils.managers import InheritanceManager

from fancypages import abstract_models


class PageType(abstract_models.AbstractPageType):
    pass


class Page(abstract_models.AbstractPage):
    pass


class Container(abstract_models.AbstractContainer):
    pass


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
