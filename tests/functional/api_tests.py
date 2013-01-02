from django.db.models import get_model
from django.utils import simplejson as json
from django.core.urlresolvers import reverse

from webtest import AppError

from fancypages import test

Container = get_model('fancypages', 'Container')


class TestTheWidgetTypeApi(test.FancyPagesWebTest):
    is_staff = True

    def setUp(self):
        super(TestTheWidgetTypeApi, self).setUp()
        self.container = Container.objects.create(variable_name="test")

    def test_is_not_available_to_anonymous_users(self):
        try:
            self.app.get(reverse('fp-api:widget-type-list'))
            self.fail('an anonymous user should not be able to use the API')
        except AppError as exc:
            self.assertIn('You do not have permission', exc.message)
            self.assertIn('403', exc.args[0])

    def test_returns_a_widget_type_form_for_container(self):
        page = self.get(
            reverse('fp-api:widget-type-list'),
            params={
                'container': self.container.id,
            }
        )
        response = json.loads(page.content)
        self.assertIn('rendered_form', response)
        self.assertIn('test_add_widget_form', response['rendered_form'])
        self.assertIn('two-column-layout', response['rendered_form'])

    def test_returns_error_when_no_container_specified(self):
        try:
            self.get(reverse('fp-api:widget-type-list'))
            self.fail(
                'a container is required, this request should raise 400 error'
            )
        except AppError as exc:
            self.assertIn('container ID is required', exc.message)
            self.assertIn('400', exc.args[0])

    def test_returns_error_when_invalid_container_is_specified(self):
        try:
            self.get(
                reverse('fp-api:widget-type-list'),
                params={
                    'container': 200,
                }
            )
            self.fail(
                'invalid container ID does not return 400 error'
            )
        except AppError as exc:
            self.assertIn('container ID is invalid', exc.message)
            self.assertIn('400', exc.args[0])
