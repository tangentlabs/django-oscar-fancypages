from django import template

from fancypages.dashboard.forms import WidgetUpdateSelectForm

register = template.Library()


class FancyContainerNode(template.Node):

    def __init__(self, container_name):
        self.container_name = template.Variable(container_name)

    def render(self, context):
        try:
            container = self.container_name.resolve(context)
        except template.VariableDoesNotExist:
            return u''

        return container.render(context.get('request', None))


@register.tag(name='fancypages-container')
def fancypages_container(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, container_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly one arguments" \
            % token.contents.split()[0]
        )
    return FancyContainerNode(container_name)


@register.assignment_tag
def update_widgets_form(page, container_name):
    container = page.get_container_from_name(container_name)
    if not container:
        return None
    return WidgetUpdateSelectForm(container)
