import pytest

from .author_base_test import AuthorTestBase
from author.views import settings_socialnetwork
from author.tests.author_base_test import sign_in_with_selenium, create_user

from app_home.tests.home_base_test import make_social_network

from utils.browser import ChromeBrowser

from selenium.webdriver.remote.webelement import WebElement

from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from time import sleep


class SocialTests(AuthorTestBase):
    def make_reverse(self) -> str:
        return reverse('author:socialnetwork')

    def make_get_request(self) -> HttpResponse:
        return self.client.get(
            self.make_reverse(),
        )

    def test_social_url_is_correct(self) -> None:
        url: str = self.make_reverse()

        self.assertEqual(
            url,
            '/author/dashboard/settings/socialnetwork/edit/'
        )

    def test_social_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            self.make_reverse()
        )

        self.assertEqual(
            response.func,
            settings_socialnetwork,
        )

    def test_social_load_correct_template(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertTemplateUsed(
            response,
            'author/partials/_socialnetwork.html'
        )

    def test_social_access_is_not_allowed_if_user_not_authenticated(self) -> None:  # noqa: E501
        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_social_access_is_allowed_if_user_is_authenticated(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.status_code,
            200,
        )


@pytest.mark.functional_test
class SocialFunctionalTests(StaticLiveServerTestCase):
    def setUp(self):
        self.url: str = self.live_server_url+reverse('author:socialnetwork')
        self.browser = ChromeBrowser(self.url)
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def enter_social_settings(self) -> None:
        make_social_network()
        create_user()
        sign_in_with_selenium(self.browser)

        button_social: WebElement = self.browser.find_element_by_xpath(
            '/html/body/main/section/nav/ul/li[1]/nav/ul/li[1]/a'
        )
        button_social.click()

    def get_input_instagram(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '//*[@id="id_instagram_link"]',
        )

    def get_dashboard(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/section',
        )

    def get_form_data(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/section/form',
        )

    def test_social_load_correct_data(self) -> None:
        self.enter_social_settings()

        self.assertEqual(
            'instagram_link',
            self.get_input_instagram().get_attribute('value'),
        )

    def test_social_save_data_after_modification(self) -> None:
        self.enter_social_settings()

        link: str = 'link_for_instagram'
        input_instagram: WebElement = self.get_input_instagram()
        input_instagram.clear()
        input_instagram.send_keys(link)

        self.get_form_data().submit()

        self.assertEqual(
            link,
            self.get_input_instagram().get_attribute('value'),
        )
        self.assertIn(
            'Dados salvos com sucesso.',
            self.get_dashboard().text,
        )

    def test_social_is_not_allowed_save_data_without_or_empty_data(self) -> None:  # noqa: E501
        self.enter_social_settings()

        self.get_input_instagram().clear()
        self.get_form_data().submit()

        sleep(3)

        self.assertIn(
            'Este campo é obrigatório.',
            self.get_dashboard().text,
        )

    def test_social_is_not_allowed_save_data_with_data_less_than_5_chars(self) -> None:  # noqa: E501
        ...
