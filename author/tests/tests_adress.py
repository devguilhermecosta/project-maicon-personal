# flake8: noqa E501
from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from author.views import settings_adress
from author.tests.author_base_test import AuthorTestBase


class AdressTests(AuthorTestBase):
    def test_settings_adress_url_is_correct(self) -> None:
        url: str = reverse('author:adress')

        self.assertEqual(url,
                         '/author/dashboard/settings/adress/',
                         )

    def test_settings_adress_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            reverse('author:adress')
        )

        self.assertEqual(response.func,
                         settings_adress,
                         )

    def test_settings_adress_load_correct_template(self) -> None:
        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('author:adress')
        )

        self.assertTemplateUsed(response,
                                'author/partials/_adress.html',
                                )

    def test_settings_adress_access_allowed_with_code_200_if_user_is_loged(self) -> None:
        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('author:adress')
        )

        self.assertEqual(response.status_code,
                         200,
                         )

    def test_settings_adress_user_is_redirected_with_code_302_if_user_is_not_loged(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('author:adress')
        )

        self.assertEqual(response.status_code,
                         302,
                         )

    def test_settings_adress_url_is_different_when_user_is_redirected(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('author:adress')
        )

        self.assertEqual(response.url,
                         '/author/login/?next=/author/dashboard/settings/adress/',
                         )

        self.fail('Testar o preenchimento automático do formulário '
                  'com o primeiro objeto do banco de dados. '
                  'Testar o POST e as mensagens de aviso.'
                  )
