from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from app_home.tests.home_base_test import make_simple_image
from . author_base_test import AuthorTestBase, make_image_object, create_user
from author.views import GalleryImageView
from gallery.models import Image
from utils.browser import make_chrome_browser
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
import shutil
import contextlib
import pytest


TEST_DIR = 'test_data'


# modify the upload location of media files
@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class GallerySettingsTests(AuthorTestBase):
    def tearDown(self) -> None:
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def test_gallery_url_is_correct(self) -> None:
        response: str = reverse('author:gallery')

        self.assertEqual(response,
                         '/author/dashboard/gallery/',
                         )

    def test_gallery_view_all_images_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            reverse('author:gallery')
        )

        self.assertEqual(response.func, GalleryImageView.all_images)

    def test_gallery_url_is_redirected_if_user_not_authenticated(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('author:gallery')
        )

        self.assertEqual(response.url,
                         '/author/login/?next=/author/dashboard/gallery/',
                         )
        self.assertEqual(response.status_code,
                         302,
                         )

    def test_gallery_panel_is_allowed_if_user_is_authenticated(self) -> None:
        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('author:gallery')
        )
        ...
        self.assertEqual(response.status_code,
                         200,
                         )

    def test_gallery_load_correct_quantity_of_images(self) -> None:
        for i in range(2):
            Image.objects.create(
                title=f'title-{i}',
                description=f'description-{i}',
                cover=make_simple_image(),
            )

        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('author:gallery')
        )

        response_content: str = response.content.decode('utf-8')

        self.assertIn('title-0', response_content)
        self.assertIn('title-1', response_content)
        self.assertIn('description-0', response_content)
        self.assertIn('description-1', response_content)
        self.assertIn('image_profile', response_content)


@pytest.mark.functional_test
@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class GallerySettingsFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser: WebDriver = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        self.browser.quit()
        return super().tearDown()

    def __enter_gallery_settings(self) -> None:
        create_user()
        make_image_object()

        self.browser.get(
            self.live_server_url +
            reverse('author:login')
            )

        input_user: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_username"]',
        )
        input_user.send_keys('username')

        input_password: WebElement = self.browser.find_element(
            By.XPATH,
            '//*[@id="id_password"]',
        )
        input_password.send_keys('password')

        button_submit: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/form/button'
        )
        button_submit.click()

        button_gallery_settings: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/nav/ul/li[2]/a',
        )

        button_gallery_settings.click()

    def __get_dashboard(self) -> WebElement:
        dasbhoard: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/section',
        )

        return dasbhoard

    def test_gallery_edit_image(self) -> None:
        self.__enter_gallery_settings()

        button_image_edit: WebElement = self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/section/section[1]/div[1]/div/a',
        )
        button_image_edit.click()

        form_image_edit: WebElement = self.browser.find_element(  # noqa: F841
            By.XPATH,
            '/html/body/main/section/section/form',
        ).submit()

        dashboard: WebElement = self.__get_dashboard()

        self.assertIn('Salvo com sucesso',
                      dashboard.text,
                      )

    def test_gallery_delete_image(self) -> None:
        self.__enter_gallery_settings()

        button_delete_image: WebElement = self.browser.find_element(  # noqa: F841 E501
            By.XPATH,
            '/html/body/main/section/section/section[1]/div/div/span/form',
        ).submit()

        alert: Alert = Alert(self.browser).accept()  # noqa: F841

        dashboard: WebElement = self.__get_dashboard()

        self.assertIn('Imagem deletada com sucesso',
                      dashboard.text,
                      )
