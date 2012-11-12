from django import template
from django.conf import settings
from django.template import defaultfilters, loader

from fancypages.dashboard import forms

register = template.Library()


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


@register.assignment_tag(takes_context=True)
def get_object_visibility(context, obj):
    try:
        return obj.is_visible
    except AttributeError:
        pass
    return True


@register.simple_tag(takes_context=True)
def render_widget_form(context, form):
    model_name = form._meta.model.__name__.lower()
    tmpl = loader.select_template([
        "fancypages/widgets/%s_form.html" % model_name,
        "fancypages/partials/editor_form_fields.html",
    ])

    context['missing_image_url'] = "%s/%s" % (
        settings.MEDIA_URL,
        getattr(settings, "OSCAR_MISSING_IMAGE_URL", '')
    )
    return tmpl.render(context)


@register.filter
def depth_as_range(depth):
    # reduce depth by 1 as treebeard root depth is 1
    return range(depth-1)
