from django.db.models import get_model

from rest_framework import serializers

Widget = get_model('fancypages', 'Widget')


class WidgetSerializer(serializers.ModelSerializer):
    display_order = serializers.IntegerField(required=False, default=0)
    #FIXME: override the model serialiser to use the actual subclass model
    # to serialise the instance rather than the model class that is provided
    # to the meta class

    def convert_object(self, obj):
        """
        Core of serialization.
        Convert an object into a dictionary of serialized field values.
        """
        ret = self._dict_class()
        ret.fields = {}

        model_fields = [f for f in obj.__class__._meta.fields if f.serialize]
        for model_field in model_fields:
            if model_field.rel and nested:
                field = self.get_nested_field(model_field)
            elif model_field.rel:
                to_many = isinstance(model_field,
                                     models.fields.related.ManyToManyField)
                field = self.get_related_field(model_field, to_many=to_many)
            else:
                field = self.get_field(model_field)

            if field:
                ret[model_field.name] = field

        for field_name, field in self.fields.items():
            field.initialize(parent=self, field_name=field_name)
            key = self.get_field_key(field_name)
            value = field.field_to_native(obj, field_name)
            ret[key] = value
            ret.fields[key] = field
        return ret

    class Meta:
        model = Widget
