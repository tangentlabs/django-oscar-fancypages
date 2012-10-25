from django import template
from django.conf import settings
from django.template import defaultfilters, loader

from fancypages.dashboard import forms

register = template.Library()


class FancyContainerNode(template.Node):

    def __init__(self, container_name):
        self.container_name = template.Variable(container_name)

    def render(self, context):
        try:
            container = self.container_name.resolve(context)
        except template.VariableDoesNotExist:
            return u''

        extra_ctx = {
            'container': container,
            'edit_mode': context.get('edit_mode', False),
        }

        form = context.get("widget_create_form", None)
        if form:
            extra_ctx['widget_create_form'] = form

        return container.render(
            context.get('request', None),
            **extra_ctx
        )


@register.tag(name='fancypages-container')
def fancypages_container(parser, token):
    # split_contents() knows not to split quoted strings.
    args = token.split_contents()

    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "%r tag requires at least one arguments" \
            % token.contents.split()[0]
        )

    tag_name, args = args[:1], args[1:]
    container_name = args.pop(0)
    return FancyContainerNode(container_name)


@register.assignment_tag
def update_widgets_form(page, container_name):
    container = page.get_container_from_name(container_name)
    if not container:
        return None
    return forms.WidgetUpdateSelectForm(container)


@register.assignment_tag
def get_add_widget_form(container):
    if not container:
        return None
    return forms.WidgetCreateSelectForm(container)


@register.simple_tag(takes_context=True)
def render_attribute(context, attr_name, *args):
    """
    Render an attribute based on editing mode.
    """
    widget = context.get('object')
    value = getattr(widget, attr_name)

    for arg in args:
        flt = getattr(defaultfilters, arg)
        if flt:
            value = flt(value)

    if not context.get('edit_mode', False):
        return unicode(value)

    wrapped_attr = u'<div id="widget-%d-%s">%s</div>'
    return wrapped_attr % (widget.id, attr_name, unicode(value))


@register.simple_tag(takes_context=True)
def render_widget_form(context, form):
    model_name = form._meta.model.__name__.lower()
    tmpl = loader.select_template([
        "fancypages/widgets/%s_form.html" % model_name,
        "fancypages/partials/editor_form_fields.html",
    ])
    context['image_asset'] = form.asset
    context['missing_image_url'] = "%s/%s" % (
        settings.MEDIA_URL,
        getattr(settings, "OSCAR_MISSING_IMAGE_URL", '')
    )
    return tmpl.render(context)


@register.filter
def depth_as_range(depth):
    # reduce depth by 1 as treebeard root depth is 1
    return range(depth-1)
