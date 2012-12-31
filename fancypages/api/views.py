from django.db.models import get_model
from django.db.models import get_model
from django.template import loader, RequestContext

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response

from fancypages.dashboard import forms
from fancypages.api import serialisers

Widget = get_model('fancypages', 'Widget')
Container = get_model('fancypages', 'Container')


class ApiV1View(APIView):

    def get(self, request):
        return Response({
            'widgets': reverse('fp-api:widget-list', request=request),
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


class WidgetTypesView(APIView):
    form_template_name = "fancypages/dashboard/widget_select.html"

    def get(self, request):
        container_id = request.QUERY_PARAMS.get('container')
        if container_id is None:
            return Response({
                    'reason': u'container ID is required for widget list',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            container = Container.objects.get(pk=container_id)
        except Container.DoesNotExist:
            return Response({
                    'reason': u'invalid container ID',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            'rendered_form': self.get_rendered_form(container),
        })

    def get_rendered_form(self, container):
        tmpl = loader.get_template(self.form_template_name)
        ctx = RequestContext(
            self.request,
            {
                'container': container,
                'add_widget_form': forms.WidgetCreateSelectForm(),
            }
        )
        return tmpl.render(ctx)
