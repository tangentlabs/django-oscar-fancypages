from django.core.exceptions import ImproperlyConfigured

from fancypages import test
from fancypages import models


class TestPageType(test.FancyPagesTestCase):

    #def test_is_generating_a_slug_from_title(self):
    #    article = models.Page()
    #    article.title = "Some Title"

    def test_empty_container_name_list_is_returned_when_unknown_page_type(self):
        page_type = models.PageType()
        page_type.template = models.PageTemplate.objects.create(
            title="Test Template",
            description="For testing",
            template_name="somewhere_else.html"
        )
        self.prepare_template_file("""{% load fancypages_tags %}
{% block main-content %}
{% fancypages-container first-container %}
{% templatetag opencomment %}
{% endblock %}
{% fancypages-container another-container %}
""")
        self.assertSequenceEqual(page_type.get_container_names(), [])

    def test_can_extract_container_names_from_template(self):
        page_type = models.PageType.objects.create(
            name='Article',
            code='article',
            template=self.template
        )
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
        page_type = models.PageType.objects.create(
            name='Article',
            code='article',
            template=self.template
        )
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

class TestAPage(test.FancyPagesTestCase):

    def test_creates_containers_when_saved(self):
        page_type = models.PageType.objects.create(
            name='Article',
            code='article',
            template=self.template
        )
        self.prepare_template_file("""{% load fancypages_tags %}
{% block main-content %}
{% fancypages-container first-container %}
{% fancypages-container second-container %}
{% templatetag opencomment %}
{% endblock %}
""")
        article_page = models.Page.objects.create(
            title='This is an article',
            page_type=page_type,
        )
        article_page.save()

        article_page = models.Page.objects.get(id=article_page.id)
        self.assertEquals(article_page.containers.count(), 2)


class TestContainer(test.FancyPagesTestCase):

    def test_can_be_assigned_to_a_page(self):
        page_type = models.PageType.objects.create(
            name='Article',
            code='article',
            template=self.template
        )

        self.prepare_template_file("{% load fancypages_tags %}"
                                   "{% fancypages-container test-container %}")

        basic_page = models.Page()
        basic_page.page_type = page_type

        container_names = page_type.get_container_names()
        self.assertEquals(container_names, [u'test-container'])

        basic_page.title = "Some Title"
        basic_page.save()

        self.assertEquals(basic_page.containers.count(), 1)

    def test_cannot_assign_multiple_instance_to_page(self):
        page_type = models.PageType.objects.create(
            name='Article',
            code='article',
            template=self.template
        )

        self.prepare_template_file("{% load fancypages_tags %}"
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
