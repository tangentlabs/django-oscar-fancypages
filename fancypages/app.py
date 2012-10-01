from django.conf.urls.defaults import patterns, url

from oscar.core.application import Application

from fancypages import views


class FancypagesApplication(Application):
    name = 'fancypages'
    #list_view = views.StoreListView
    #detail_view = views.StoreDetailView

    def get_urls(self):
        urlpatterns = super(FancypagesApplication, self).get_urls()

        urlpatterns += patterns('',
        #    url(r'^$', self.list_view.as_view(), name='index'),
        #    url(r'^(?P<slug>[\w-]+)/$', self.detail_view.as_view(), name='detail'),
        )
        return self.post_process_urls(urlpatterns)


application = FancypagesApplication()
