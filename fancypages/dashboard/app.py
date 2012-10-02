from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

from oscar.core.application import Application
from oscar.apps.dashboard.nav import register, Node

from fancypages.dashboard import views


node = Node(_('Page Manager'))
node.add_child(Node(_('Pages'), 'fancypages-dashboard:page-list'))
node.add_child(Node(_('Page Types'), 'fancypages-dashboard:page-type-list'))
register(node, 100)


class FancypagesDashboardApplication(Application):
    name = 'fancypages-dashboard'
    page_type_list_view = views.PageTypeListView
    page_type_create_view = views.PageTypeCreateView
    page_type_update_view = views.PageTypeUpdateView
    page_type_delete_view = views.PageTypeDeleteView

    page_list_view = views.PageListView
    page_create_redirect_view = views.PageCreateRedirectView
    page_create_view = views.PageCreateView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'types/$', self.page_type_list_view.as_view(),
                name='page-type-list'),
            url(r'type/create/$', self.page_type_create_view.as_view(),
                name='page-type-create'),
            url(r'type/update/(?P<pk>\d+)/$', self.page_type_update_view.as_view(),
                name='page-type-update'),
            url(r'type/delete/(?P<pk>\d+)/$', self.page_type_delete_view.as_view(),
                name='page-type-delete'),

            url(r'^$', self.page_list_view.as_view(), name='page-list'),
            url(r'create/$',
                self.page_create_redirect_view.as_view(), name='page-create'),
            url(r'create/(?P<page_type_code>[\w-]+)/$',
                self.page_create_view.as_view(), name='page-create'),
        )
        return self.post_process_urls(urlpatterns)


application = FancypagesDashboardApplication()
