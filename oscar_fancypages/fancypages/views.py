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
        if not self.object.page_type:
            return [self.DEFAULT_TEMPLATE]
        return [self.object.page_type.template_name]

    def get_object(self):
        try:
            return FancyPage.objects.get(slug=self.kwargs.get('slug'))
        except (FancyPage.DoesNotExist, FancyPage.MultipleObjectsReturned):
            raise Http404

    def get_context_data(self, **kwargs):
        ctx = super(FancyPageEditorMixin, self).get_context_data(**kwargs)
        if self.object:
            ctx['object'] = self.object
            for container in Container.get_containers(self.object):
                ctx[container.name] = container
        return ctx


class FancyPageDetailView(FancyPageEditorMixin, ProductCategoryView):
    context_object_name = 'fancypage'

    def get_context_data(self, **kwargs):
        context = super(FancyPageDetailView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.object
        context['object'] = self.object
        context['summary'] = self.object.name
        return context

    def get_categories(self):
        """
        Return a list of the current page/category and it's ancestors
        """
        categories = [self.object]
        categories.extend(list(self.object.get_descendants()))
        return categories

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        try:
            self.object = FancyPage.objects.get(slug=slug)
        except FancyPage.DoesNotExist:
            raise Http404()
        response = super(FancyPageDetailView, self).get(request, *args, **kwargs)

        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404

        return response


class FancyHomeView(FancyPageEditorMixin, ProductCategoryView):
    model = FancyPage

    HOMEPAGE_NAME = getattr(settings, 'FP_HOMEPAGE_NAME', 'Home')

    def get(self, request, *args, **kwargs):
        self.kwargs.setdefault('category_slug', slugify(self.HOMEPAGE_NAME))
        self.object = self.get_object()
        response = super(FancyHomeView, self).get(request, *args, **kwargs)
        if request.user.is_staff:
            return response

        if not self.object.is_visible:
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
