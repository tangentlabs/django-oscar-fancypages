from django.conf.urls.defaults import patterns, url, include

import fancypages.api.urls
from fancypages.app import application as fancypages_app
from fancypages.dashboard.app import application as dashboard_app

urlpatterns = patterns('',
    url(r'^', include(fancypages_app.urls)),
    url(r'^dashboard/fancypages/', include(dashboard_app.urls)),
    url(fancypages.api.API_BASE_URL, include(fancypages.api.urls)),
)
