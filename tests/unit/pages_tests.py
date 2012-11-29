from django.core.exceptions import ImproperlyConfigured

from fancypages import test
from fancypages import models
from fancypages.utils import get_container_names_from_template


class TestContainerNames(test.FancyPagesTestCase):

    def test_can_be_extracted_from_template(self):
        self.prepare_template_file("""{% load fp_container_tags %}
{% block main-content %}
{% fancypages_container first-container %}
{% templatetag opencomment %}
{% endblock %}
{% fancypages_container another-container %}
""")
        self.assertSequenceEqual(
            get_container_names_from_template(self.template_name),
            [u'first-container', u'another-container']
        )

    def test_cannot_be_duplicated_in_template(self):
        self.prepare_template_file("""{% load fp_container_tags %}
{% block main-content %}
{% fancypages_container first-container %}
{% fancypages_container first-container %}
{% templatetag opencomment %}
{% endblock %}
""")
        self.assertRaises(
            ImproperlyConfigured,
            get_container_names_from_template,
            self.template_name
        )

class TestAPage(test.FancyPagesTestCase):

    def test_creates_containers_when_saved(self):
        self.prepare_template_file("""{% load fp_container_tags %}
{% block main-content %}
{% fancypages_container first-container %}
{% fancypages_container second-container %}
{% templatetag opencomment %}
{% endblock %}
""")
        article_page = models.Page.add_root(
            title='This is an article',
            template_name=self.template_name,
        )

        article_page = models.Page.objects.get(id=article_page.id)
        self.assertEquals(article_page.containers.count(), 2)


class TestContainer(test.FancyPagesTestCase):

    def setUp(self):
        super(TestContainer, self).setUp()
        self.prepare_template_file("{% load fp_container_tags %}"
                                   "{% fancypages_container test-container %}")

        self.page = models.Page.add_root(
            title="Some Title",
            template_name=self.template_name
        )
        self.container_names = get_container_names_from_template(
            self.page.template_name
        )

    def test_can_be_assigned_to_a_page(self):
        self.assertEquals(self.container_names, [u'test-container'])
        self.assertEquals(self.page.containers.count(), 1)

    def test_cannot_assign_multiple_instance_to_page(self):
        self.assertEquals(self.container_names, [u'test-container'])

        self.page.create_container(self.container_names[0])
        self.assertEquals(self.page.containers.count(), 1)

        self.page.create_container(self.container_names[0])
        self.assertEquals(self.page.containers.count(), 1)

    def test_can_be_retrieved_from_page_and_variable_name(self):
        container = models.Container.get_container_by_name(self.page,
                                                           'test-container')
        self.assertEquals(
            container.variable_name,
            self.page.containers.all()[0].variable_name
        )
        self.assertEquals(self.page.containers.count(), 1)
