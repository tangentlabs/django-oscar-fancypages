from django.http import Http404
from django.conf import settings
from django.db.models import get_model

from oscar.apps.catalogue.views import ProductCategoryView

Page = get_model('fancypages', 'Page')
Category = get_model('catalogue', 'Category')
Container = get_model('fancypages', 'Container')


class PageEditorMixin(object):

    def get_object(self):
        try:
            return Page.objects.get(category__slug=self.kwargs.get('slug'))
        except (Page.DoesNotExist, Page.MultipleObjectsReturned):
            raise Http404

    def get_context_data(self, **kwargs):
        if self.object:
            for container in Container.get_containers(self.object):
                kwargs[container.variable_name] = container
        return super(PageEditorMixin, self).get_context_data(**kwargs)


class PageDetailView(PageEditorMixin, ProductCategoryView):
    context_object_name = 'fancypage'

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['summary'] = self.category.name
        return context

    def get_categories(self):
        """
        Return a list of the current category and it's ancestors
        """
        categories = [self.category]
        categories.extend(list(self.category.get_descendants()))
        return categories

    def get_template_names(self):
        if not self.object.page_type:
            return [settings.FP_DEFAULT_TEMPLATE]
        return [self.object.page_type.template_name]

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['category_slug']
        try:
            self.object = Page.objects.get(category__slug=slug)
        except Page.DoesNotExist:
            raise Http404()
        try:
            self.category = self.object.category
        except Page.DoesNotExist:
            raise Http404()
        response = super(PageDetailView, self).get(request, *args, **kwargs)

        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404

        return response


class FancyHomeView(PageEditorMixin, ProductCategoryView):
    model = Page

    def get(self, request, *args, **kwargs):
        self.kwargs.setdefault('category_slug', 'home')
        self.object = self.get_object()
        response = super(FancyHomeView, self).get(request, *args, **kwargs)
        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404

        return response

    def get_object(self):
        try:
            page = Page.objects.get(category__slug='home')
        except Page.DoesNotExist:
            page = Category.add_root(name='Home', slug='home').page
        return page
