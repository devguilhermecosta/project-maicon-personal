# flake8: noqa
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from author.views import settings_adress
from author.tests.author_base_test import AuthorTestBase
from app_home.tests.home_base_test import make_adress
from parameterized import parameterized


class AdressTests(AuthorTestBase):
    def make_reverse(self) -> reverse:
        return reverse('author:adress')

    def make_get_request(self) -> HttpResponse:
        return self.client.get(
            self.make_reverse(),
        )

    def make_post_request(self, data, follow: bool = False) -> HttpResponse:
        return self.client.post(
            self.make_reverse(),
            data=data,
            follow=follow,
        )

    def setUp(self) -> None:
        self.adress_data: dict = {
            'name': 'this is the adress',
            'adress': 'thi is the street',
            'city': 'this is the city',
            'postal': 'this is the postal',
        }

        return super().setUp()

    def test_settings_adress_url_is_correct(self) -> None:
        url: str = self.make_reverse()

        self.assertEqual(url,
                         '/author/dashboard/settings/adress/',
                         )

    def test_settings_adress_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            self.make_reverse(),
        )

        self.assertEqual(response.func,
                         settings_adress,
                         )

    def test_settings_adress_load_correct_template(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertTemplateUsed(response,
                                'author/partials/_adress.html',
                                )

    def test_settings_adress_access_allowed_with_code_200_if_user_is_loged(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertEqual(response.status_code,
                         200,
                         )

    def test_settings_adress_user_is_redirected_with_code_302_if_user_is_not_loged(self) -> None:
        response: HttpResponse = self.make_get_request()

        self.assertEqual(response.status_code,
                         302,
                         )

    def test_settings_adress_url_is_different_when_user_is_redirected(self) -> None:
        adress = make_adress()
        response: HttpResponse = self.make_get_request()

        self.assertEqual(response.url,
                         '/author/login/?next=/author/dashboard/settings/adress/',
                         )


    def test_settings_adress_form_used_first_object_created(self) -> None:
        self.make_login()

        adress_data: dict = {
            'name': 'this is the adress',
            'adress': 'thi is the street',
            'city': 'this is the city',
            'postal': 'this is the postal',
        }
        
        make_adress(**adress_data)

        response: HttpResponse = self.make_get_request()

        response_content: str = response.content.decode('utf-8')

        for key, value in adress_data.items():
            self.assertIn(value, response_content)


    @parameterized.expand([
        ('name', 'Este campo é obrigatório'),
        ('adress', 'Este campo é obrigatório'),
        ('city', 'Este campo é obrigatório'),
        ('postal', 'Este campo é obrigatório'),
    ])
    def test_settings_adress_form_used_fields_cannot_be_empty(self,
                                                              field,
                                                              message,
                                                              ) -> None:
        self.make_login()

        self.adress_data[field] = ''

        response: HttpResponse = self.make_post_request(
            data=self.adress_data,
            follow=True
        )

        response_content: str = response.content.decode('utf-8')

        self.assertIn(message, response_content)
        
    def test_settings_adress_form_used_return_message_success_if_data_ok(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_post_request(
            data=self.adress_data,
            follow=True,
        )

        response_content: str = response.content.decode('utf-8')
        message_succes: str = 'Dados salvos com sucesso'

        self.assertIn(message_succes, response_content)
