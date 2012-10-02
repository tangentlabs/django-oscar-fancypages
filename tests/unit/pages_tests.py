import os
import tempfile

from django.conf import settings
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from fancypages import models


class TestPageType(TestCase):

    def setUp(self):
        tempdir = tempfile.gettempdir()
        self.default_template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = list(settings.TEMPLATE_DIRS) + [tempdir]
        self.template_name = 'test_article_page.html'
        self.template_file = os.path.join(tempdir, self.template_name)

    def tearDown(self):
        # make sure that other tests don't rely on these settings
        settings.TEMPLATE_DIRS = self.default_template_dirs

    def prepare_template_file(self, content):
        with open(self.template_file, 'w') as tmpl_file:
            tmpl_file.write(content)

    #def test_is_generating_a_slug_from_title(self):
    #    article = models.Page()
    #    article.title = "Some Title"

    def test_empty_container_name_list_is_returned_when_unknown_page_type(self):
        page_type = models.PageType()
        self.prepare_template_file("""{% load fancypages_tags %}
{% block main-content %}
{% fancypages-container first-container %}
{% templatetag opencomment %}
{% endblock %}
{% fancypages-container another-container %}
""")
        self.assertSequenceEqual(page_type.get_container_names(), [])

    def test_can_extract_container_names_from_template(self):
        page_type = models.PageType.objects.create(name='Article', code='article',
                                                   template_name=self.template_name)
        self.prepare_template_file("""{% load fancypages_tags %}
{% block main-content %}
{% fancypages-container first-container %}
{% templatetag opencomment %}
{% endblock %}
{% fancypages-container another-container %}
""")
        self.assertSequenceEqual(
            page_type.get_container_names(),
            [u'first-container', u'another-container']
        )

    def test_cannot_be_used_with_duplicate_container_names(self):
        page_type = models.PageType.objects.create(name='Article', code='article',
                                                   template_name=self.template_name)

        self.prepare_template_file("""{% load fancypages_tags %}
{% block main-content %}
{% fancypages-container first-container %}
{% fancypages-container first-container %}
{% templatetag opencomment %}
{% endblock %}
""")
        self.assertRaises(
            ImproperlyConfigured,
            page_type.get_container_names
        )


class TestContainer(TestCase):

    def setUp(self):
        tempdir = tempfile.gettempdir()
        self.default_template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = list(settings.TEMPLATE_DIRS) + [tempdir]

        __, self.template_path = tempfile.mkstemp(suffix=".html")
        self.template_name = os.path.basename(self.template_path)

    def tearDown(self):
        # make sure that other tests don't rely on these settings
        settings.TEMPLATE_DIRS = self.default_template_dirs

    def test_can_be_assigned_to_a_page(self):
        page_type = models.PageType.objects.create(
            name='Article', code='article',
            template_name=self.template_name
        )

        with open(self.template_path, 'w') as fh:
            fh.write("{% load fancypages_tags %}"
                     "{% fancypages-container test-container %}")

        basic_page = models.Page()
        basic_page.page_type = page_type

        container_names = page_type.get_container_names()
        self.assertEquals(container_names, [u'test-container'])

        basic_page.title = "Some Title"
        basic_page.save()

        basic_page.containers.create(variable_name=container_names[0])
        basic_page.save()

        self.assertEquals(basic_page.containers.count(), 1)

    def test_cannot_assign_multiple_instance_to_page(self):
        page_type = models.PageType.objects.create(
            name='Article', code='article',
            template_name=self.template_name
        )

        with open(self.template_path, 'w') as fh:
            fh.write("{% load fancypages_tags %}"
                     "{% fancypages-container test-container %}")

        basic_page = models.Page()
        basic_page.page_type = page_type

        container_names = page_type.get_container_names()
        self.assertEquals(container_names, [u'test-container'])

        basic_page.title = "Some Title"
        basic_page.save()

        basic_page.create_container(container_names[0])
        self.assertEquals(basic_page.containers.count(), 1)

        basic_page.create_container(container_names[0])
        self.assertEquals(basic_page.containers.count(), 1)
