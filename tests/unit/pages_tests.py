import os
import tempfile

from django.conf import settings
from django.test import TestCase

from fancypages.pages import models


class TestAPage(TestCase):

    def test_can_extract_container_names_from_template(self):
        tempdir = tempfile.gettempdir()
        template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = list(settings.TEMPLATE_DIRS) + [tempdir]
        template_name = 'test_article_page.html'

        article = models.ArticlePage()
        article.template_name = template_name

        with open(os.path.join(tempdir, template_name), 'w') as tmpl_file:
            tmpl_file.write("""{% load fancypages_tags %}
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

        # make sure that other tests don't rely on these settings
        settings.TEMPLATE_DIRS = template_dirs
