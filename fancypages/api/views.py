from django.db.models import get_model

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response

from fancypages.api import serialisers

Widget = get_model('fancypages', 'Widget')


class ApiV1View(APIView):

    def get(self, request):
        """
        The entry endpoint of our API.
        """
        return Response({
            'widgets': reverse('widget-list', request=request),
            #'groups': reverse('group-list', request=request),
        })


class WidgetListView(generics.ListCreateAPIView):
    model = Widget
    serializer_class = serialisers.WidgetSerializer

    def get_queryset(self):
        return super(WidgetListView, self).get_queryset().select_subclasses()


class WidgetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    model = Widget
    serializer_class = serialisers.WidgetSerializer

    def get_object(self):
        return self.model.objects.get_subclass(
            id=self.kwargs.get(self.pk_url_kwarg)
        )
