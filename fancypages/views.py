from django.http import Http404
from django.views.generic import DetailView

from fancypages import models


class PageEditorMixin(object):
    edit_mode = False

    def get_context_data(self, **kwargs):
        kwargs.update({
            'edit_mode': self.edit_mode,
        })
        if self.object and hasattr(self.object, 'containers'):
            for container in self.object.containers.all():
                kwargs[container.variable_name] = container
        return super(PageEditorMixin, self).get_context_data(**kwargs)


class PageDetailView(PageEditorMixin, DetailView):
    model = models.Page
    context_object_name = "page"

    def get(self, request, *args, **kwargs):
        response = super(PageDetailView, self).get(request, *args, **kwargs)

        if request.user.is_staff:
            return response

        if not self.object.is_visible:
            raise Http404

        return response

    def get_template_names(self):
        return [
            self.object.page_type.template.template_name,
        ]
