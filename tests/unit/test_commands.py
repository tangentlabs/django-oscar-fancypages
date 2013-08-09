import mock

from django.test import TestCase
from django.db.models import get_model
from django.core.management import call_command

Category = get_model('catalogue', 'Category')
FancyPage = get_model('fancypages', 'FancyPage')


class TestPageCreatorCommand(TestCase):

    def setUp(self):
        super(TestPageCreatorCommand, self).setUp()
        self.category = Category.add_root(name="Test Category")
        self.assertEquals(Category.objects.count(), 1)
        self.assertEquals(FancyPage.objects.count(), 0)


    def test_can_generate_pages_running_as_command(self):
        call_command('fp_create_pages_for_categories')
        self._check_fancypage_created_correctly()

    def test_can_generate_pages_using_frozen_orm(self):
        def get_orm_model(self, name):
            return get_model(*name.split('.'))
        mock_orm = mock.Mock()
        mock_orm.__getitem__ = get_orm_model

        call_command('fp_create_pages_for_categories', orm=mock_orm)
        self._check_fancypage_created_correctly()

    def _check_fancypage_created_correctly(self):
        self.assertEquals(Category.objects.count(), 1)
        self.assertEquals(FancyPage.objects.count(), 1)

        fancypage = FancyPage.objects.all()[0]
        self.assertEquals(fancypage.name, self.category.name)
        self.assertEquals(fancypage.path, self.category.path)
