from django.conf.urls.defaults import patterns, url, include

from oscar.core.application import Application
from oscar.views.decorators import staff_member_required

from fancypages.dashboard import views
from fancypages.assets.app import application as assets_app


class FancypagesDashboardApplication(Application):
    name = 'fp-dashboard'
    assets_app = assets_app

    page_list_view = views.PageListView
    page_create_view = views.PageCreateView
    page_update_view = views.PageUpdateView
    page_delete_view = views.PageDeleteView
    page_customise_view = views.PageCustomiseView
    page_preview_view = views.PagePreviewView
    page_select_view = views.PageSelectView

    widget_update_view = views.WidgetUpdateView
    widget_delete_view = views.WidgetDeleteView

    content_customise_view = views.ContentCustomiseView
    content_preview_view = views.ContentPreviewView

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^assets/', include(self.assets_app.urls)),

            url(
                r'^$',
                self.page_list_view.as_view(),
                name='page-list'
            ),
            url(
                r'^create/$',
                self.page_create_view.as_view(),
                name='page-create'
            ),
            url(
                r'^create/(?P<parent_pk>\d+)/$',
                self.page_create_view.as_view(),
                name='child-page-create'
            ),
            url(
                r'^update/(?P<pk>\d+)/$',
                self.page_update_view.as_view(),
                name='page-update'
            ),
            url(
                r'^delete/(?P<pk>\d+)/$',
                self.page_delete_view.as_view(),
                name='page-delete'
            ),

            url(
                r'^customise/(?P<pk>\d+)/$',
                self.page_customise_view.as_view(),
                name='page-customise'
            ),
            url(
                r'^preview/(?P<slug>[\w-]+(/[\w-]+)*)/$',
                self.page_preview_view.as_view(),
                name='page-preview'
            ),

            url(
                r'^selector/$',
                self.page_select_view.as_view(),
                name='page-select'
            ),

            url(
                r'^widget/update/(?P<pk>\d+)/$',
                self.widget_update_view.as_view(),
                name='widget-update'
            ),
            url(
                r'^widget/delete/(?P<pk>\d+)/$',
                self.widget_delete_view.as_view(),
                name='widget-delete'
            ),
            url(
                r'^content/(?P<content_type_pk>\d+)/customise/(?P<pk>\d+)/$',
                self.content_customise_view.as_view(),
                name='content-customise'
            ),
            url(
                r'^content/(?P<content_type_pk>\d+)/preview/(?P<pk>\d+)/$',
                self.content_preview_view.as_view(),
                name='content-preview'
            ),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = FancypagesDashboardApplication()
