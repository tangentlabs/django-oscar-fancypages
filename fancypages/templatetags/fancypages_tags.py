from django import template

register = template.Library()


class FancyContainerNode(template.Node):

    def __init__(self, container_name):
        self.container_name = template.Variable(container_name)

    def render(self, context):
        return ''


@register.tag(name='fancypages-container')
def fancypages_container(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, container_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires exactly one arguments" % token.contents.split()[0])
    return FancyContainerNode(container_name)
