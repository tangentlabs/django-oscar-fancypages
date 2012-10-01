from django.db.models import get_model
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django_webtest import WebTest

PageType = get_model('fancypages', 'PageType')


class PageWebTest(WebTest):
    username = 'testuser'
    email = 'testuser@example.com'
    password = 'mysecretpassword'
    is_anonymous = True
    is_staff = False

    def setUp(self):
        super(PageWebTest, self).setUp()
        self.user = None

        if self.is_staff:
            self.is_anonymous = False

        if self.is_staff or not self.is_anonymous:
            self.user = User.objects.create_user(username=self.username,
                                                 email=self.email,
                                                 password=self.password)
            self.user.is_staff = self.is_staff
            self.user.save()

    def get(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs['user'] = self.user
        return self.app.post(*args, **kwargs)


class TestAStaffMember(PageWebTest):
    is_staff = True

    def setUp(self):
        super(TestAStaffMember, self).setUp()
        self.article_type = PageType.objects.create(name='Article', code='article',
                                template_name="")
        self.other_type = PageType.objects.create(name='Other', code='other',
                                                  template_name="")

    def test_can_see_a_list_of_page_types(self):
        page = self.get(reverse('fancypages-dashboard:page-list'))

        self.assertContains(page, 'Article')
        self.assertContains(page, 'Other')

    def test_can_create_a_new_article_page(self):
        page = self.get(reverse('fancypages-dashboard:page-list'))

        type_form = page.form
        type_form['page_type'] = self.article_type.code
        page = type_form.submit()

        self.assertRedirects(
            page,
            reverse(
                'fancypages-dashboard:page-create',
                args=(self.article_type.code,)
            ),
            status_code=301
        )
        page = page.follow()
        self.assertContains(page, "Create new 'Article' page")
