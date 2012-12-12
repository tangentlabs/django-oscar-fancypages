from django.http import Http404
from django.db.models import get_model
from django.views.generic import DetailView
from django.contrib.sites.models import Site

Page = get_model('fancypages', 'Page')
Container = get_model('fancypages', 'Container')


class PageEditorMixin(object):
    edit_mode = False

    def get_context_data(self, **kwargs):
        kwargs.update({
            'edit_mode': self.edit_mode,
        })
        if self.object:
            for container in Container.get_containers(self.object):
                kwargs[container.variable_name] = container
        return super(PageEditorMixin, self).get_context_data(**kwargs)


class PageDetailView(PageEditorMixin, DetailView):
    model = Page
    context_object_name = "page"

    def get_object(self, queryset=None):
        current_site = Site.objects.get_current()
        page = self.model.objects.get(
            slug=self.kwargs.get('slug', None),
        )
        if (page.display_on_sites.all()
            and current_site not in page.display_on_sites.all()):
            raise Http404("page is not visible on this page")
        return page

    def get(self, request, *args, **kwargs):
        response = super(PageDetailView, self).get(request, *args, **kwargs)

        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404

        return response

    def get_template_names(self):
        return [self.object.template_name]
