import pytest
import shutil
import contextlib
from django.http import HttpResponse
from django.urls import ResolverMatch, resolve, reverse
from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from author.views import settings_profile
from .author_base_test import (
    AuthorTestBase,
    sign_in_with_selenium,
    create_user,
    )
from app_home.tests.home_base_test import make_profle
from utils.browser import ChromeBrowser
from selenium.webdriver.remote.webelement import WebElement


class ProfileSettingsTests(AuthorTestBase):
    def make_reverse(self) -> str:
        return reverse('author:profile')

    def make_get_request(self) -> HttpResponse:
        return self.client.get(
            self.make_reverse(),
        )

    def test_profile_url_is_correct(self) -> None:
        url: str = self.make_reverse()

        self.assertEqual(
            url,
            '/author/dashboard/settings/profile/edit/'
        )

    def test_profile_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            self.make_reverse()
        )

        self.assertEqual(
            response.func,
            settings_profile,
        )

    def test_profile_view_load_correct_template(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertTemplateUsed(
            response,
            'author/partials/_settings.html'
        )

    def test_profile_url_is_redirected_if_user_not_authenticated(self) -> None:
        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.url,
            '/author/login/?next=/author/dashboard/settings/profile/edit/'
        )
        self.assertEqual(
            response.status_code,
            302,
        )

    def test_profile_status_code_200_if_user_is_authenticated(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.status_code,
            200,
        )


TEST_DIR: str = 'test_data'


@pytest.mark.functional_test
@override_settings(MEDIA_ROOT=TEST_DIR + '/media')
class ProfileSettingsFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        create_user()
        self.url: str = self.live_server_url+reverse('author:login')
        self.browser: ChromeBrowser = ChromeBrowser(
            self.url,
        )
        return super().tearDown()

    def tearDown(self) -> None:
        self.browser.quit()

        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def enter_profile_settings_with_content(self) -> None:
        make_profle()
        sign_in_with_selenium(self.browser)

        button_profile: WebElement = self.browser.find_element_by_xpath(
            '/html/body/main/section/nav/ul/li[1]/nav/ul/li[3]/a',
        )
        button_profile.click()

    def get_title(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '//*[@id="id_title"]',
        )

    def get_description(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '//*[@id="id_description"]',
        )

    def get_image(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/section/form/div[3]/a',
        )

    def get_dashboard(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/section',
        )

    def get_form_data(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/section/form',
        )

    def test_profile_load_correct_data(self) -> None:
        self.enter_profile_settings_with_content()

        input_title: WebElement = self.get_title()

        input_description: WebElement = self.get_description()

        link_image: WebElement = self.get_image()

        self.assertIn(
            'profile_title',
            input_title.get_attribute('value'),
        )
        self.assertIn(
            'profile_description',
            input_description.get_attribute('value'),
        )
        self.assertIn(
            'media/app_home/images/profile/image_profile',
            link_image.get_attribute('href'),
        )

    def test_profile_save_data_after_modification(self) -> None:
        self.enter_profile_settings_with_content()

        new_title: str = 'This is the new title'
        input_title: WebElement = self.get_title()
        input_title.clear()
        input_title.send_keys(new_title)

        form: WebElement = self.get_form_data()
        form.submit()

        title_changed: WebElement = self.get_title()
        dashboard: WebElement = self.get_dashboard()

        self.assertIn(
            new_title,
            title_changed.get_attribute('value'),
        )
        self.assertIn(
            'Dados salvos com sucesso.',
            dashboard.text,
        )

    def test_profile_saving_with_empty_data_is_not_allowed(self) -> None:
        self.enter_profile_settings_with_content()

        input_title: WebElement = self.get_title()
        input_title.clear()

        form: WebElement = self.get_form_data()
        form.submit()

        dashboard: WebElement = self.get_dashboard()

        self.assertIn(
            'Este campo é obrigatório',
            dashboard.text,
        )
