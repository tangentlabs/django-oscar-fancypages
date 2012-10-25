from django.conf.urls.defaults import patterns, url

from oscar.core.application import Application
from oscar.views.decorators import staff_member_required

from fancypages.assets import views


class AssetApplication(Application):
    name = 'fp-assets'
    image_list_view = views.ImageListView
    image_create_view = views.ImageCreateView

    def get_urls(self):
        urlpatterns = super(AssetApplication, self).get_urls()

        urlpatterns += patterns('',
            url(r'^images/$',
                self.image_list_view.as_view(), name='image-list'),
            url(r'^image/upload/$',
                self.image_create_view.as_view(), name='image-upload'),
        )
        return self.post_process_urls(urlpatterns)

    def get_url_decorator(self, url_name):
        return staff_member_required


application = AssetApplication()
