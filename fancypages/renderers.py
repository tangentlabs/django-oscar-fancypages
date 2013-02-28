from copy import copy

from django import template
from django.template import loader
from django.core.exceptions import ImproperlyConfigured

from fancypages.models.base import Widget, Container


class ContainerRenderer(object):

    def __init__(self, container, context, extra_context=None):
        if not container and not issubclass(container, Container):
            raise TypeError(
                "widget must be a subclass of 'Widget' not '%s'" % type(container)
            )
        if not extra_context:
            extra_context = {}
        self.container = container
        self.context = copy(context)
        self.context.update(extra_context)

    def get_context_data(self, **kwargs):
        return kwargs

    def render(self):
        """
        Render the container and all its contained widgets.
        """
        ordered_widgets = self.container.widgets.select_subclasses()

        tmpl = loader.select_template(self.container.get_template_names())

        rendered_widgets = []
        for widget in ordered_widgets:
            renderer = widget.get_renderer_class()(widget, self.context)
            try:
                rendered_widget = renderer.render()
            except ImproperlyConfigured:
                continue
            rendered_widgets.append((widget.id, rendered_widget))

        self.context['container'] = self.container
        self.context['rendered_widgets'] = rendered_widgets
        self.context.update(self.get_context_data())
        return tmpl.render(self.context)


class WidgetRenderer(object):
    #FIXME: needs to be renamed to 'widget' to prevent collision in context
    context_object_name = 'object'

    def __init__(self, widget, context, extra_context=None):
        if not widget and not issubclass(widget, Widget):
            raise TypeError(
                "widget must be a subclass of 'Widget' not '%s'" % type(widget)
            )
        if not extra_context:
            extra_context = {}
        self.widget = widget
        self.context = copy(context)
        self.context.update(extra_context)

    def get_context_data(self, **kwargs):
        return kwargs

    def render(self):
        if not self.widget.get_template_names():
            raise ImproperlyConfigured(
                "a template name is required for a widget to be rendered"
            )
        try:
            tmpl = loader.select_template(self.widget.get_template_names())
        except template.TemplateDoesNotExist:
            return u''

        self.context[self.context_object_name] = self.widget
        self.context.update(self.get_context_data())
        return tmpl.render(self.context)
