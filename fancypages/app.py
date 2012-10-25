from django.conf.urls.defaults import patterns, url, include

from oscar.core.application import Application

from fancypages import views
from fancypages.assets.app import application as assets_app


class FancypagesApplication(Application):
    name = 'fancypages'

    assets_app = assets_app

    page_detail_view = views.PageDetailView

    def get_urls(self):
        urlpatterns = super(FancypagesApplication, self).get_urls()

        urlpatterns += patterns('',
            url(r'^page/(?P<slug>[\w-]+(/[\w-]+)*)/$',
                self.page_detail_view.as_view(), name='page-detail'),
            url(r'^assets/', include(self.assets_app.urls)),
        )
        return self.post_process_urls(urlpatterns)


application = FancypagesApplication()
