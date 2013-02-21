from django.core.exceptions import ImproperlyConfigured
from django.template import loader, RequestContext, Context

from fancypages.models.base import Widget, Container


class ContainerRenderer(object):

    def __init__(self, container, context):
        if not container and not issubclass(container, Container):
            raise TypeError(
                "widget must be a subclass of 'Widget' not '%s'" % type(container)
            )
        self.container = container
        self.page_context = context
        self.request = self.page_context.get('request')

    def render(self, **kwargs):
        """
        Render the container and all its contained widgets.
        """
        ordered_widgets = self.container.widgets.select_subclasses()

        tmpl = loader.get_template(self.container.template_name)

        if self.request:
            ctx = RequestContext(self.request)
        else:
            ctx = Context()

        ctx['container'] = self
        ctx['rendered_widgets'] = []

        for widget in ordered_widgets:
            renderer = widget.get_renderer_class()(widget, self.page_context)
            try:
                rendered_widget = renderer.render(**kwargs)
            except ImproperlyConfigured:
                continue

            ctx['rendered_widgets'].append((widget.id, rendered_widget))

        ctx.update(kwargs)
        return tmpl.render(ctx)


class WidgetRenderer(object):
    context_object_name = 'object'

    def __init__(self, widget, context):
        if not widget and not issubclass(widget, Widget):
            raise TypeError(
                "widget must be a subclass of 'Widget' not '%s'" % type(widget)
            )
        self.widget = widget
        self.page_context = context
        self.request = self.page_context.get('request')

    def get_context_data(self):
        return {}

    def render(self, **kwargs):
        if not self.widget.template_name:
            raise ImproperlyConfigured(
                "a template name is required for a widget to be rendered"
            )

        if self.request:
            ctx = RequestContext(self.request)
        else:
            ctx = Context()

        ctx[self.context_object_name] = self.widget
        ctx.update(kwargs)
        ctx.update(self.get_context_data())
        tmpl = loader.get_template(self.widget.template_name)
        return tmpl.render(ctx)
