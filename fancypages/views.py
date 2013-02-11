from django.http import Http404
from django.conf import settings
from django.db.models import get_model

from oscar.apps.catalogue.views import ProductCategoryView

Page = get_model('fancypages', 'Page')
Container = get_model('fancypages', 'Container')


class PageEditorMixin(object):
    edit_mode = False

    def get_object(self):
        try:
            return Page.objects.get(category__slug=self.kwargs.get('slug'))
        except (Page.DoesNotExist, Page.MultipleObjectsReturned):
            raise Http404

    def get_context_data(self, **kwargs):
        kwargs.update({
            'edit_mode': self.edit_mode,
        })
        if self.object:
            for container in Container.get_containers(self.object):
                kwargs[container.variable_name] = container
        return super(PageEditorMixin, self).get_context_data(**kwargs)


class PageDetailView(PageEditorMixin, ProductCategoryView):

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['object'] = self.object
        context['page'] = self.object
        return context

    def get_template_names(self):
        if not self.object.page_type:
            return [settings.FP_DEFAULT_TEMPLATE]
        return [self.object.page_type.template_name]

    def get(self, request, *args, **kwargs):
        self.object = self.get_categories()[0].page
        response = super(PageDetailView, self).get(request, *args, **kwargs)

        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404

        return response


class FancyHomeView(PageDetailView):
    model = Page

    def get(self, request, *args, **kwargs):
        self.kwargs.setdefault('category_slug', 'home')
        return super(FancyHomeView, self).get(request, *args, **kwargs)

    def get_object(self):
        try:
            page = Page.objects.get(category__slug='home')
        except Page.DoesNotExist:
            page = Page.add_root(name='Home', slug='home')
        return page
