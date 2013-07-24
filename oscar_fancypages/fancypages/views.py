from django.http import Http404
from django.conf import settings
from django.db.models import get_model
from django.template.defaultfilters import slugify

from oscar.apps.catalogue.views import ProductCategoryView

FancyPage = get_model('fancypages', 'FancyPage')
Category = get_model('catalogue', 'Category')
Container = get_model('fancypages', 'Container')


class FancyPageEditorMixin(object):
    DEFAULT_TEMPLATE = getattr(settings, 'FP_DEFAULT_TEMPLATE')

    def get_template_names(self):
        if not self.category.page_type:
            return [self.DEFAULT_TEMPLATE]
        return [self.category.page_type.template_name]

    def get_object(self):
        try:
            return FancyPage.objects.get(slug=self.kwargs.get('slug'))
        except (FancyPage.DoesNotExist, FancyPage.MultipleObjectsReturned):
            raise Http404

    def get_context_data(self, **kwargs):
        ctx = super(FancyPageEditorMixin, self).get_context_data(**kwargs)
        if self.category:
            ctx['object'] = self.category
            for container in Container.get_containers(self.category):
                ctx[container.name] = container
        return ctx


class FancyPageDetailView(FancyPageEditorMixin, ProductCategoryView):
    context_object_name = 'fancypage'

    def get_context_data(self, **kwargs):
        context = super(FancyPageDetailView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.category
        context['object'] = self.category
        context['summary'] = self.category.name
        return context

    def get_categories(self):
        """
        Return a list of the current page/category and it's ancestors
        """
        categories = [self.category]
        categories.extend(list(self.category.get_descendants()))
        return categories

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            self.category = FancyPage.objects.get(slug=slug)
        except FancyPage.DoesNotExist:
            raise Http404()
        response = super(FancyPageDetailView, self).get(request, *args, **kwargs)

        if request.user.is_staff:
            return response

        if not self.category.is_visible:
            raise Http404

        return response


class FancyHomeView(FancyPageEditorMixin, ProductCategoryView):
    model = FancyPage

    HOMEPAGE_NAME = getattr(settings, 'FP_HOMEPAGE_NAME', 'Home')

    def get(self, request, *args, **kwargs):
        self.kwargs.setdefault('category_slug', slugify(self.HOMEPAGE_NAME))
        self.category = self.get_object()
        response = super(FancyHomeView, self).get(request, *args, **kwargs)
        if request.user.is_staff:
            return response

        if not self.category.is_visible:
            raise Http404

        return response

    def get_object(self):
        slug = slugify(self.HOMEPAGE_NAME)
        try:
            page = FancyPage.objects.get(slug=slug)
        except FancyPage.DoesNotExist:
            page = FancyPage.add_root(
                name=self.HOMEPAGE_NAME,
                slug=slug,
                status=FancyPage.PUBLISHED,
            )
        return page
