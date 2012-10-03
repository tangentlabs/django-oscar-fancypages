from django.conf.urls.defaults import patterns, url

from oscar.core.application import Application

from fancypages import views


class FancypagesApplication(Application):
    name = 'fancypages'
    page_detail_view = views.PageDetailView

    def get_urls(self):
        urlpatterns = super(FancypagesApplication, self).get_urls()

        urlpatterns += patterns('',
            url(r'^page/(?P<code>[\w-]+)/$',
                self.page_detail_view.as_view(), name='page-detail'),
        )
        return self.post_process_urls(urlpatterns)


application = FancypagesApplication()
