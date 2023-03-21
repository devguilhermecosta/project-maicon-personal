from django.test import override_settings
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .author_base_test import (
    AuthorTestBase, create_user, sign_in_with_selenium
    )
from author.views.initial_gallery import settings_initial_gallery
from app_home.tests.home_base_test import make_pre_gallery
from app_home.models import PreGallery
from utils.browser import make_chrome_browser
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import pytest
import contextlib
import shutil


TEST_DIR = 'test_data'


class InitialGalleryTests(AuthorTestBase):
    def _make_get_request(self) -> HttpResponse:
        response: HttpResponse = self.client.get(
            reverse('author:initialgallery')
        )
        return response

    def test_initial_gallery_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            reverse('author:initialgallery')
        )
        self.assertEqual(response.func, settings_initial_gallery)

    def test_initial_gallery_url_is_correct(self) -> None:
        url: str = reverse('author:initialgallery')

        self.assertEqual(url,
                         '/author/dashboard/settings/initial-gallery/edit/',
                         )

    def test_initial_gallery_url_is_diferent_if_user_not_authenticated(self) -> None:  # noqa: E501
        response: HttpResponse = self._make_get_request()

        self.assertEqual(response.url,
                         '/author/login/?next=/author/dashboard/settings/initial-gallery/edit/',  # noqa: E501
                         )

    def test_initial_gallery_status_code_302_if_user_not_authenticated(self) -> None:  # noqa: E501
        response: HttpResponse = self._make_get_request()

        self.assertEqual(response.status_code, 302)

    def test_initial_gallery_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        self.make_login()

        response: HttpResponse = self._make_get_request()

        self.assertEqual(response.status_code,
                         200,
                         )

    def test_initial_gallery_load_correct_template(self) -> None:
        self.make_login()
        response: HttpResponse = self._make_get_request()

        self.assertTemplateUsed(response,
                                'author/partials/_initialgallery.html',
                                )


@override_settings(MEDIA_ROOT=TEST_DIR + '/media')
@pytest.mark.functional_test
class InitialGalleryFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        create_user()
        self.browser: WebDriver = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def _enter_gallery_with_content(self) -> None:
        """
        Enter the image pre gallery with an instance
        of PreGallery and logged in.
        """
        make_pre_gallery()

        self.browser.get(
            self.live_server_url+reverse('author:initialgallery')
        )

        sign_in_with_selenium(self.browser)

    def test_initial_gallery_load_correct_data_into_form(self) -> None:
        self._enter_gallery_with_content()

        pre_gallery_settings: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/nav/ul/li[1]/nav/ul/li[4]/a',
        )
        pre_gallery_settings.click()

        input_title: WebElement = self.browser.find_element(
            By.ID,
            'id_title',
        )
        textarea: WebElement = self.browser.find_element(
            By.ID,
            'id_description'
        )
        image: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/section/form/div[3]/a',
        )

        self.assertIn('pre_gallery_title',
                      input_title.get_attribute('value'),
                      )
        self.assertIn('pre_gallery_description',
                      textarea.get_attribute('value'),
                      )
        self.assertIn('app_home/images/pre-gallery/image_profile',
                      image.get_attribute('href'),
                      )
