from django.contrib import admin
from django.conf.urls import patterns, include, url

from oscar.app import shop

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include(shop.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
