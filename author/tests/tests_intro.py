from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.http import HttpResponse
from django.urls import ResolverMatch, resolve, reverse
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from app_home.tests.home_base_test import make_section_intro
from author.views import settings_sectionintro
from utils.browser import make_chrome_browser

from .author_base_test import (AuthorTestBase, create_user,
                               sign_in_with_selenium)
import pytest


class SectionIntroTests(AuthorTestBase):
    def make_reverse(self) -> HttpResponse:
        return reverse('author:sectionintro')

    def client_make_get(self) -> HttpResponse:
        return self.client.get(
            self.make_reverse()
        )

    def test_intro_url_is_correct(self) -> None:
        url: str = self.make_reverse()

        self.assertEqual(
            '/author/dashboard/settings/sectionintro/edit/',
            url,
        )

    def test_intro_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            self.make_reverse()
        )

        self.assertEqual(
            response.func,
            settings_sectionintro,
        )

    def test_intro_url_is_different_if_user_not_authenticated(self) -> None:
        response: HttpResponse = self.client_make_get()

        self.assertEqual(
            response.url,
            '/author/login/?next=/author/dashboard/settings/sectionintro/edit/'
        )

    def test_intro_status_code_is_302_if_user_not_authenticated(self) -> None:
        response: HttpResponse = self.client_make_get()

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_intro_status_code_is_200_if_user_is_authenticated(self) -> None:
        self.make_login()

        response: HttpResponse = self.client_make_get()

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_intro_load_correct_template(self) -> None:
        self.make_login()
        response: HttpResponse = self.client_make_get()

        self.assertTemplateUsed(
            response,
            'author/partials/_sectionintro.html'
        )


@pytest.mark.functional_test
class SectionIntroFunctionalTests(StaticLiveServerTestCase):
    def setUp(self, *args, **kwargs) -> None:
        create_user()
        self.browser: WebDriver = make_chrome_browser()
        self.browser.get(
            self.live_server_url+reverse('author:sectionintro')
        )
        return super().setUp(*args, **kwargs)

    def tearDown(self, *args, **kwargs) -> None:
        self.browser.quit()
        return super().tearDown(*args, **kwargs)

    def get_input_title_webelement(self) -> WebElement:
        input_title: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_title"]',
        )
        return input_title

    def get_dashboard_element(self) -> WebElement:
        dashboard: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/section',
        )
        return dashboard

    def get_form_data(self) -> WebElement:
        form: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/section/form',
        )
        return form

    def enter_the_intro_with_content(self) -> None:
        make_section_intro()

        sign_in_with_selenium(self.browser)

        button_intro: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/nav/ul/li[1]/nav/ul/li[2]/a',
        )
        button_intro.click()

    def test_intro_load_correct_content(self) -> None:
        self.enter_the_intro_with_content()

        input_title: WebElement = self.get_input_title_webelement()

        input_description: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_description"]',
        )

        self.assertIn(
            'section_intro_title',
            input_title.get_attribute('value'),
        )
        self.assertIn(
            'section_intro_description',
            input_description.get_attribute('value'),
        )

    def test_intro_save_data_after_mod_and_show_message(self) -> None:
        self.enter_the_intro_with_content()

        input_title: WebElement = self.get_input_title_webelement()
        input_title.clear()
        new_content: str = 'this is the new title'
        input_title.send_keys(
            new_content,
        )

        form: WebElement = self.get_form_data()
        form.submit()

        input_title_after_mod: WebElement = self.get_input_title_webelement()

        dashboard: WebElement = self.get_dashboard_element()

        self.assertIn(
            new_content,
            input_title_after_mod.get_attribute('value'),
        )
        self.assertIn(
            'Dados salvos com sucesso.',
            dashboard.text,
        )

    def test_intro_does_not_allow_saving_data_without_data(self) -> None:
        self.enter_the_intro_with_content()

        input_title: WebElement = self.get_input_title_webelement()
        input_title.clear()

        form: WebElement = self.get_form_data()
        form.submit()

        dashboard: WebElement = self.get_dashboard_element()

        self.assertIn(
            'Este campo é obrigatório.',
            dashboard.text
        )
