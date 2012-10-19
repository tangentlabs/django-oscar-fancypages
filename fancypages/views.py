from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from fancypages import models


class PageEditorMixin(object):
    edit_mode = False

    def get_context_data(self, **kwargs):
        kwargs = {
            'edit_mode': False,
        }
        kwargs.update(kwargs)
        return kwargs


class PageDetailView(PageEditorMixin, DetailView):
    model = models.Page
    context_object_name = "page"

    def get_object(self):
        return get_object_or_404(
            self.model,
            code=self.kwargs.get('code', None)
        )

    def get_context_data(self, **kwargs):
        ctx = super(PageDetailView, self).get_context_data(**kwargs)
        for container in self.object.containers.all():
            ctx[container.variable_name] = container
        return ctx

    def get_template_names(self):
        return [
            self.object.page_type.template.template_name,
        ]
