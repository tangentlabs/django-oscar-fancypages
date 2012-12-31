from django.conf.urls.defaults import patterns, url

from fancypages.api import views


urlpatterns = patterns('',
    url(r'^$', views.ApiV1View.as_view(), name="api-root"),
    url(r'^widgets$', views.WidgetListView.as_view(), name='widget-list'),
    url(
        r'^widget/(?P<pk>\d+)$',
        views.WidgetRetrieveUpdateDestroyView.as_view(),
        name='widget-retrieve-update-destroy'
    ),
)
