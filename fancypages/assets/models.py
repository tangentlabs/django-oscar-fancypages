from django.db import models


class AbstractAsset(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    description = models.TextField(default="")
    creator = models.ForeignKey('auth.User')

    #keywords = models.CharField(max_length=255)
    #shared_by = models.ForeignKey('auth.User', related_name="shared_assets", null=True)
    #is_global = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class ImageAsset(AbstractAsset):
    image = models.ImageField(
        upload_to='asset/images/%Y/%m',
        width_field='width',
        height_field='height'
    )
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    size = models.IntegerField(blank=True, null=True) # Bytes

    @property
    def asset_type(self):
        return self._meta.object_name.lower()

    def get_absolute_url(self):
        return self.image.url
