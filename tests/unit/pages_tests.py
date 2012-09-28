import os
import tempfile

from django.conf import settings
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from fancypages.pages import models


class TestArticlePage(TestCase):

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

    def test_can_extract_container_names_from_template(self):
        article = models.ArticlePage()
        article.template_name = self.template_name
        self.prepare_template_file("""{% load fancypages_tags %}
{% block main-content %}
{% fancypages-container first-container %}
{% templatetag opencomment %}
{% endblock %}
{% fancypages-container another-container %}
""")
        self.assertSequenceEqual(
            article.get_container_names(),
            [u'first-container', u'another-container']
        )

    def test_cannot_be_used_with_duplicate_container_names(self):
        article = models.ArticlePage()
        article.template_name = self.template_name
        self.prepare_template_file("""{% load fancypages_tags %}
{% block main-content %}
{% fancypages-container first-container %}
{% fancypages-container first-container %}
{% templatetag opencomment %}
{% endblock %}
""")
        self.assertRaises(
            ImproperlyConfigured,
            article.get_container_names
        )
