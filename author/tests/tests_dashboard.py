from . author_base_test import AuthorTestBase
from django.test import override_settings
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from author import views
from app_home.tests.home_base_test import make_home_content
import contextlib
import shutil


TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class DashboardTests(AuthorTestBase):
    def make_reverse(self) -> reverse:
        return reverse('author:dashboard')

    def make_get_request(self) -> HttpResponse:
        return self.client.get(
            self.make_reverse(),
        )

    def tearDown(self) -> None:
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def test_dashboard_url_is_correct(self) -> None:
        url: str = self.make_reverse()

        self.assertEqual(url, '/author/dashboard/')

    def test_dashboard_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            self.make_reverse(),
        )

        self.assertEqual(response.func, views.dashboard)

    def test_dashboard_url_is_redirected_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.url,
            '/author/login/?next=/author/dashboard/'
            )
        self.assertEqual(
            response.status_code,
            302,
        )

    def test_dashboard_status_code_200_if_user_is_authenticated(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertEqual(response.status_code, 200)

    def test_dashboard_context_load_correct_data(self) -> None:
        self.make_login()

        name: str = 'this is the title footer'

        make_home_content(option_name=name)

        response: HttpResponse = self.make_get_request()

        response_content: str = response.content.decode('utf-8')

        self.assertIn(
            name,
            response_content
            )

    def test_dashboard_load_correct_template(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertTemplateUsed(
            response,
            'author/pages/dashboard.html'
        )
