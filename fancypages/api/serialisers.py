import re

from django.db.models import get_model
from django.forms.models import modelform_factory
from django.template import loader, RequestContext

from rest_framework import serializers

from fancypages.dashboard import forms

Widget = get_model('fancypages', 'Widget')


class WidgetSerializer(serializers.ModelSerializer):
    update_form_template = "fancypages/dashboard/widget_update.html"

    display_order = serializers.IntegerField(required=False, default=0)
    form_markup = serializers.SerializerMethodField('get_widget_form')

    def get_form_class(self, obj):
        model = obj.__class__
        form_class = getattr(
            forms,
            "%sForm" % model.__name__,
            forms.WidgetForm
        )
        return modelform_factory(model, form=form_class)

    def get_widget_form(self, obj):
        request = self.context.get('request')
        if not request or 'includeForm' not in request.GET:
            return u''

        tmpl = loader.get_template(self.update_form_template)
        ctx = RequestContext(
            self.context['request'],
            {
                'object': obj,
                'widget': obj,
                'form': self.get_form_class(obj)(instance=obj)
            }
        )
        return tmpl.render(ctx)

    class Meta:
        model = Widget
