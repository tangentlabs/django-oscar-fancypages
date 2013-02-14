import warnings

from django import template
from django.db.models import get_model
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.contenttypes.models import ContentType


register = template.Library()


class ContainerNodeMixin(object):

    def get_object(self, context):
        if not self.object_name:
            return None
        try:
            return self.object_name.resolve(context)
        except template.VariableDoesNotExist:
            pass
        return None

    def get_container(self, context):
        Container = get_model('fancypages', 'Container')
        # check first if the container name refers to a
        # variable in the context and use it a container
        try:
            return self.container_name.resolve(context)
        except template.VariableDoesNotExist:
            pass
        # container variable is not in the context. we have to look
        # up the container from the variable name and - if the object
        # is not None - the object the container is attached to.
        try:
            return Container.get_container_by_name(
                name=self.container_name.var,
                obj=self.object,
            )
        except KeyError:
            pass
        return None

    def render(self, context):
        """
        Render the container provided by the ``container_name`` variable
        name in this node. If a node with this name exists in the
        context, the context variable will be used as container. Otherwise,
        we try to retrieve a container based on the variable name using
        the ``object`` variable in the context.
        """
        self.object = self.get_object(context)
        self.container = self.get_container(context)

        if not self.container:
            return u''

        extra_ctx = {
            'container': self.container,
            'edit_mode': context.get('edit_mode', False),
        }

        form = context.get("widget_create_form", None)
        if form:
            extra_ctx['widget_create_form'] = form

        return self.container.render(
            context.get('request', None),
            **extra_ctx
        )


class FancyContainerNode(ContainerNodeMixin, template.Node):

    def __init__(self, container_name):
        self.container_name = template.Variable(container_name)
        self.object_name = None


class FancyObjectContainerNode(ContainerNodeMixin, template.Node):

    def __init__(self, container_name, object_name):
        self.container_name = template.Variable(container_name)
        self.object_name = template.Variable(object_name or 'object')


@register.tag
def fp_container(parser, token):
    # split_contents() knows not to split quoted strings.
    args = token.split_contents()

    if len(args) != 2:
        raise template.TemplateSyntaxError(
            "%r tag expects a single argument container" \
            % token.contents.split()[0]
        )

    tag_name, args = args[:1], args[1:]
    container_name = args.pop(0)
    return FancyContainerNode(container_name)


@register.tag
def fp_object_container(parser, token):
    # split_contents() knows not to split quoted strings.
    args = token.split_contents()

    if len(args) < 2 or len(args) > 4:
        raise template.TemplateSyntaxError(
            "%r tag requires container name as first argument and "
            " optionally object" % token.contents.split()[0]
        )

    tag_name, args = args[:1], args[1:]
    container_name = args.pop(0)
    try:
        object_name = args.pop(0)
    except IndexError:
        object_name = None
    return FancyObjectContainerNode(container_name, object_name)


@register.tag
def fancypages_container(parser, token):
    warnings.warn(
        "template tag 'fancypages_container' is deprecated please use"
        "'fp_object_container' instead",
        PendingDeprecationWarning
    )
    return fp_object_container(parser, token)


@register.simple_tag(takes_context=True)
def get_customise_url(context, instance=None):
    if not instance:
        instance = context.get('object', None)

    if instance is None:
        return u''

    try:
        content_type = ContentType.objects.get_for_model(instance)
    except AttributeError:
        return u''

    try:
        return reverse('fp-dashboard:content-customise', kwargs={
            'content_type_pk': content_type.id,
            'pk': instance.id,
        })
    except NoReverseMatch:
        return u''


@register.simple_tag(takes_context=True)
def get_preview_url(context, instance=None):
    if not instance:
        instance = context.get('object', None)

    if instance is None:
        return u''

    try:
        content_type = ContentType.objects.get_for_model(instance)
    except AttributeError:
        return u''

    try:
        return reverse('fp-dashboard:content-preview', kwargs={
            'content_type_pk': content_type.id,
            'pk': instance.id,
        })
    except NoReverseMatch:
        return u''
