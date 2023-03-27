from django.http import HttpResponse
from django.urls import ResolverMatch, resolve, reverse
from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from author.views import settings_profile

from .author_base_test import AuthorTestBase, create_user
from app_home.tests.home_base_test import make_profle

from utils.browser import make_chrome_browser

import pytest
import shutil
import contextlib

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

from time import sleep


class ProfileSettingsTests(AuthorTestBase):
    def test_profile_url_is_correct(self) -> None:
        url: str = reverse('author:profile')

        self.assertEqual(
            url,
            '/author/dashboard/settings/profile/edit/'
        )

    def test_profile_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            reverse('author:profile')
        )

        self.assertEqual(
            response.func,
            settings_profile,
        )

    def test_profile_view_load_correct_template(self) -> None:
        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('author:profile')
        )

        self.assertTemplateUsed(
            response,
            'author/partials/_profile.html'
        )

    def test_profile_url_is_redirected_if_user_not_authenticated(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('author:profile')
        )

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

        response: HttpResponse = self.client.get(
            reverse('author:profile'),
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        ...


TEST_DIR: str = 'test_data'


@pytest.mark.functional_test
@override_settings(MEDIA_ROOT=TEST_DIR + '/media')
class ProfileSettingsFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser: WebDriver = make_chrome_browser()
        return super().tearDown()

    def tearDown(self) -> None:
        self.browser.quit()

        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def enter_profile_settings_with_content(self) -> None:
        create_user()
        make_profle()

        self.browser.get(
            self.live_server_url+reverse('author:login')
        )

        input_username: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_username"]',
        )
        input_username.send_keys('username')

        input_password: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_password"]',
        )
        input_password.send_keys('password')

        form: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section[1]/form',
        )
        form.submit()

        button_profile: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/nav/ul/li[1]/nav/ul/li[3]/a',
        )
        button_profile.click()

    def get_title(self) -> WebElement:
        return self.browser.find_element(
            By.XPATH,
            '//*[@id="id_title"]',
        )

    def get_description(self) -> WebElement:
        return self.browser.find_element(
            By.XPATH,
            '//*[@id="id_description"]',
        )

    def get_image(self) -> WebElement:
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/section/form/div[3]/a',
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
        self.fail('make tests from profile edit')
