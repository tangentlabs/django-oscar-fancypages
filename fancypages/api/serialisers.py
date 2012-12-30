from django.db.models import get_model

from rest_framework import serializers

Widget = get_model('fancypages', 'Widget')


class WidgetSerializer(serializers.ModelSerializer):
    display_order = serializers.IntegerField(required=False, default=0)
    #FIXME: override the model serialiser to use the actual subclass model
    # to serialise the instance rather than the model class that is provided
    # to the meta class

    class Meta:
        model = Widget
