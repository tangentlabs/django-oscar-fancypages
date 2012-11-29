from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns, url, include

from oscar.core.application import Application
from oscar.apps.dashboard.nav import register, Node
from oscar.views.decorators import staff_member_required

from fancypages.dashboard import views
from fancypages.assets.app import application as assets_app


node = Node(_('Page Manager'))
node.add_child(Node(
    _('Pages'),
    'fp-dashboard:page-list')
)
node.add_child(Node(
    _('Page Types'),
    'fp-dashboard:page-type-list')
)
node.add_child(Node(
    _('Page Templates'),
    'fp-dashboard:page-template-list')
)
register(node, 100)


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

    product_page_customise_view = views.ProductPageCustomiseView
    product_page_preview_view = views.ProductPagePreviewView

    container_add_widget_view = views.ContainerAddWidgetView

    widget_select_view = views.WidgetSelectView
    widget_update_view = views.WidgetUpdateView
    widget_delete_view = views.WidgetDeleteView
    widget_move_view = views.WidgetMoveView
    widget_add_tab_view = views.WidgetAddTabView

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
                r'^container/(?P<pk>\d+)/add/(?P<code>[\w-]+)/$',
                self.container_add_widget_view.as_view(),
                name='container-add-widget'
            ),

            url(
                r'^widget/(?P<container_id>\d+)/select/$',
                self.widget_select_view.as_view(),
                name='widget-select'),
            url(
                r'^widget/update/(?P<pk>\d+)/$',
                self.widget_update_view.as_view(),
                name='widget-update'),
            url(
                r'^widget/delete/(?P<pk>\d+)/$',
                self.widget_delete_view.as_view(),
                name='widget-delete'),
            url(
                r'^widget/move/(?P<pk>\d+)/to/(?P<container_pk>\d+)/(?P<index>\d+)/$',
                self.widget_move_view.as_view(),
                name='widget-move'),
            url(
                r'^widget/(?P<pk>\d+)/add-tab/$',
                self.widget_add_tab_view.as_view(),
                name='widget-add-tab'),

            url(
                r'^product/customise/(?P<pk>\d+)/$',
                self.product_page_customise_view.as_view(),
                name='product-page-customise'
            ),
            url(
                r'^product/preview/(?P<pk>\d+)/$',
                self.product_page_preview_view.as_view(),
                name='product-page-preview'
            ),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = FancypagesDashboardApplication()
