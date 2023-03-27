from .author_base_test import AuthorTestBase
from .author_base_test import create_user
from author.views import login_view
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import pytest


class LoginTests(AuthorTestBase):
    def test_login_url_is_correct(self) -> None:
        url: str = reverse('author:login')

        self.assertEqual(
            url,
            '/author/login/'
        )

    def test_login_view_function_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            reverse('author:login')
        )

        self.assertEqual(
            response.func,
            login_view,
        )

    def test_login_load_correct_template(self) -> None:
        self.client.get(
            reverse('author:login')
        )

        self.assertTemplateUsed(
            'author/pages/login.html',
        )

    def test_login_status_code_200(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('author:login')
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_login_create_return_404_if_request_is_get(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('author:login_create')
        )

        self.assertEqual(
            response.status_code,
            404,
        )


@pytest.mark.functional_test
class LoginFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser: WebDriver = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def login_dashboard_without_user(self) -> None:
        self.browser.get(
            self.live_server_url+reverse('author:login')
        )

        input_user: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_username"]',
        )
        input_user.send_keys(
            'username',
        )

        input_password: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_password"]',
        )
        input_password.send_keys(
            'password',
        )

        form_login: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/form',
        )

        form_login.submit()

    def test_login_not_allowed_if_invalid_credentials(self) -> None:
        self.login_dashboard_without_user()

        main: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main',
        )

        self.assertIn(
            'Usuário ou senha inválidos',
            main.text,
        )

    def test_login_is_allowed_if_user_is_authenticated(self) -> None:
        create_user()

        self.login_dashboard_without_user()

        dashboard: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section',
        )

        self.assertIn(
            'Configurações do site',
            dashboard.text,
        )
