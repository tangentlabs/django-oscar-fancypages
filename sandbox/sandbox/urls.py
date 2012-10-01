from django.contrib import admin
from django.conf.urls import patterns, include, url

from oscar.app import shop

from fancypages.app import application as fancypages_app
from fancypages.dashboard.app import application as dashboard_app

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(shop.urls)),

    url(r'^dashboard/fancypages/', include(dashboard_app.urls)),
    url(r'^fancypages/', include(fancypages_app.urls)),

    url(r'^admin/', include(admin.site.urls)),
)
