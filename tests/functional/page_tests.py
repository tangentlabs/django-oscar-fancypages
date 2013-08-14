import os
import shutil
import tempfile

from PIL import Image

from django.db.models import get_model
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from oscar_testsupport.testcases import WebTestCase

FancyPage = get_model('fancypages', 'FancyPage')

TEMP_IMAGE_DIR = tempfile.mkdtemp(suffix='_page_tests_images')
TEMP_MEDIA_ROOT = tempfile.mkdtemp(suffix='_page_tests_media')


class TestHomePage(WebTestCase):

    def setUp(self):
        super(TestHomePage, self).setUp()

    def test_is_created_when_no_home_page_exists(self):
        self.assertEquals(FancyPage.objects.count(), 0)
        home_page = self.app.get(reverse('home'))
        self.assertEquals(FancyPage.objects.count(), 1)

        fancypage = FancyPage.objects.all()[0]
        context = home_page.context[0]

        self.assertIn('page-container', context)
        self.assertEquals(context.get('object').id, fancypage.id)
        self.assertEquals(fancypage.containers.count(), 1)

        container = fancypage.containers.all()[0]
        self.assertEquals(type(container.page_object), type(fancypage))
        self.assertEquals(container.page_object.id, fancypage.id)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TestAFancyPage(WebTestCase):
    is_staff = True

    def tearDown(self):
        super(TestAFancyPage, self).tearDown()
        if os.path.exists(TEMP_MEDIA_ROOT):
            shutil.rmtree(TEMP_MEDIA_ROOT)
        if os.path.exists(TEMP_IMAGE_DIR):
            shutil.rmtree(TEMP_IMAGE_DIR)

    def test_can_be_updated_with_an_image(self):
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

        category_path = os.path.join(TEMP_MEDIA_ROOT, 'categories')
        fancy_page = FancyPage.objects.get(id=fancy_page.id)
        self.assertEquals(
            fancy_page.image.path,
            os.path.join(category_path, filename.rsplit('/')[-1])
        )
