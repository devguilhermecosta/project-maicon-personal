from django.http import HttpResponse
from django.urls import ResolverMatch, resolve, reverse
from author.views import LogoutView
from .author_base_test import AuthorTestBase


class LogoutTests(AuthorTestBase):
    def test_logout_url_is_correct(self) -> None:
        url: str = reverse('author:logout')

        self.assertEqual(
            url,
            '/author/logout/'
        )

    def test_logout_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            reverse('author:logout')
        )

        self.assertEqual(
            response.func.view_class,
            LogoutView,
        )

    def test_logout_url_is_redirected_if_user_not_authenticated_and_method_post(self) -> None:  # noqa: E501
        response: HttpResponse = self.client.post(
            reverse('author:logout'),
        )

        self.assertEqual(
            response.status_code,
            302
        )
        self.assertEqual(
            response.url,
            '/author/login/?next=/author/logout/'
        )

    def test_logout_url_is_redirected_if_user_not_authenticated_and_method_get(self) -> None:  # noqa: E501
        response: HttpResponse = self.client.get(
            reverse('author:logout'),
        )

        self.assertEqual(
            response.status_code,
            302,
        )
        self.assertEqual(
            response.url,
            '/author/login/?next=/author/logout/'
        )

    def test_logout_status_code_405_if_method_get_and_user_is_authenticated(self) -> None:  # noqa: E501
        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('author:logout')
        )

        self.assertEqual(
            response.status_code,
            405,
        )

    def test_logout_url_is_correct_if_user_is_authenticated(self) -> None:
        self.make_login()

        response: HttpResponse = self.client.post(
            reverse('author:logout'),
        )

        self.assertEqual(
            response.url,
            '/author/login/'
        )

    def test_logout_content_has_logout_succesfully_if_logout(self) -> None:
        self.make_login()

        response: HttpResponse = self.client.post(
            reverse('author:logout'),
            follow=True,
        )

        response_content: str = response.content.decode('utf-8')

        self.assertIn(
            'Logout realizado com sucesso.',
            response_content,
        )
