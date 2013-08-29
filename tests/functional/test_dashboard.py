import os
import shutil
import tempfile

from PIL import Image

from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from fancypages import test

PageType = get_model('fancypages', 'PageType')
FancyPage = get_model('fancypages', 'FancyPage')

TEMP_IMAGE_DIR = tempfile.mkdtemp(suffix='_page_tests_images')
TEMP_MEDIA_ROOT = tempfile.mkdtemp(suffix='_page_tests_media')


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestAnImageForAFancyPage(test.FancyPagesWebTest):
    is_staff = True

    def tearDown(self):
        super(TestAnImageForAFancyPage, self).tearDown()
        if os.path.exists(TEMP_MEDIA_ROOT):
            shutil.rmtree(TEMP_MEDIA_ROOT)
        if os.path.exists(TEMP_IMAGE_DIR):
            shutil.rmtree(TEMP_IMAGE_DIR)

    def test_can_be_added_in_the_dashboard(self):
        fancy_page = FancyPage.add_root(name='Sample Page')
        self.assertEquals(fancy_page.image, None)

        im = Image.new("RGB", (320, 240), "red")

        __, filename = tempfile.mkstemp(suffix='.jpg', dir=TEMP_IMAGE_DIR)
        im.save(filename, "JPEG")

        page = self.get(
            reverse('fp-dashboard:page-update', args=(fancy_page.id,))
        )

        settings_form = page.form
        settings_form['image'] = (filename,)
        list_page = settings_form.submit()

        self.assertRedirects(list_page, reverse('fp-dashboard:page-list'))

        pages_path = os.path.join(TEMP_MEDIA_ROOT, 'categories')
        fancy_page = FancyPage.objects.get(id=fancy_page.id)
        self.assertEquals(
            fancy_page.image.path,
            os.path.join(pages_path, filename.rsplit('/')[-1])
        )
