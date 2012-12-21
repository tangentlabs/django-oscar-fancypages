from django.db import models

from fancypages.models.base import Container


class OrderedContainer(Container):
    display_order = models.PositiveIntegerField()

    def __unicode__(self):
        return u"Container #%d '%s' in '%s'" % (
            self.display_order,
            self.variable_name,
            self.content_type
        )

    class Meta:
        app_label = 'fancypages'
