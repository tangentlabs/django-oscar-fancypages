from django.db.models import get_model
from django.core.urlresolvers import reverse

from django_webtest import WebTest

FancyPage = get_model('fancypages', 'FancyPage')


class TestHomePage(WebTest):

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
