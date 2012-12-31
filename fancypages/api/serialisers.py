from django.db.models import get_model
from django.forms.models import modelform_factory
from django.template import loader, RequestContext

from rest_framework import serializers

from fancypages.dashboard import forms

Widget = get_model('fancypages', 'Widget')


class RenderFormFieldMixin(object):
    form_template_name = None
    context_object_name = 'object'

    def get_rendered_form(self, obj):
        request = self.context.get('request')
        if not request or 'includeForm' not in request.GET:
            return u''

        form_class = self.get_form_class(obj)
        form_kwargs = self.get_form_kwargs(obj)

        tmpl = loader.get_template(self.form_template_name)
        ctx = RequestContext(
            self.context['request'],
            {
                self.context_object_name: obj,
                'form': form_class(**form_kwargs),
            }
        )
        return tmpl.render(ctx)

    def get_form_kwargs(self, obj):
        return {
            'instance': obj,
        }

    def get_form_class(self, obj):
        return modelform_factory(obj.__class__)


class WidgetSerializer(RenderFormFieldMixin, serializers.ModelSerializer):
    form_template_name = "fancypages/dashboard/widget_update.html"
    context_object_name = 'widget'

    display_order = serializers.IntegerField(required=False, default=0)
    code = serializers.CharField(required=True)
    rendered_form = serializers.SerializerMethodField('get_rendered_form')

    def restore_object(self, attrs, instance=None):
        code = attrs.pop('code')

        if instance is None and code is not None:
            widget_class = self.get_widget_class(code)
            if widget_class:
                self.opts.model = widget_class

        return super(WidgetSerializer, self).restore_object(attrs, instance)

    def get_widget_class(self, code):
        model = None
        for widget_class in Widget.itersubclasses():
            if widget_class._meta.abstract:
                continue

            if widget_class.code == code:
                model = widget_class
                break
        return model

    def get_form_class(self, obj):
        model = obj.__class__
        form_class = getattr(
            forms,
            "%sForm" % model.__name__,
            forms.WidgetForm
        )
        return modelform_factory(model, form=form_class)

    class Meta:
        model = Widget
