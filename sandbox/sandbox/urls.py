from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include, url

from oscar.app import shop

import fancypages.urls
from fancypages.views import FancyHomeView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', FancyHomeView.as_view(), name='home'),
    url(r'^', include(shop.urls)),
    url(r'^', include(fancypages.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
