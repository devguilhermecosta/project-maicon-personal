import pytest

from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from author.tests.author_base_test import (
    AuthorTestBase,
    sign_in_with_selenium,
    create_user,
    )

from author.views.services import ServiceView, ServiceDeleteView

from app_home.tests.home_base_test import make_queryset_services
from app_home.models import Service

from utils.browser import ChromeBrowser

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.alert import Alert


class ServicesTests(AuthorTestBase):
    def make_get_request(self) -> HttpResponse:
        return self.client.get(
            reverse('author:services')
        )

    def test_services_url_is_correct(self) -> None:
        url: str = reverse('author:services')

        self.assertEqual(
            url,
            '/author/dashboard/settings/services/'
        )

    def test_service_crete_is_correct(self) -> None:
        url: str = reverse('author:new_service')

        self.assertEqual(
            url,
            '/author/dashboard/settings/services/new/'
        )

    def test_services_delete_url_is_correct(self) -> None:
        url: str = reverse(
            'author:service_delete',
            args=(1,),
            )

        self.assertEqual(
            url,
            '/author/dashboard/settings/services/delete/1/',
        )

    def test_service_edit_is_corret(self) -> None:
        url: str = reverse(
            'author:service_edit',
            args=(1,),
            )

        self.assertEqual(
            url,
            '/author/dashboard/settings/services/1/edit/',
        )

    def test_services_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            reverse('author:services'),
        )

        self.assertEqual(
            response.func,
            ServiceView.all_services,
        )

    def test_services_delete_view_is_correct(self) -> None:
        response: HttpResponse = resolve(
            reverse('author:service_delete', args=(1,))
        )
        self.assertEqual(
            response.func.view_class,
            ServiceDeleteView,
        )

    def test_services_load_correct_template(self) -> None:
        self.make_login()
        response: HttpResponse = self.make_get_request()

        self.assertTemplateUsed(
            response,
            'author/partials/_all_services.html'
        )

    def test_services_url_is_redirected_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.status_code,
            302
        )

    def test_services_access_is_allowed_if_user_is_authenticated(self) -> None:
        self.make_login()

        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.status_code,
            200,
        )


@pytest.mark.functional_test
class ServicesFunctionalTests(StaticLiveServerTestCase):
    def setUp(self) -> None:
        create_user()
        make_queryset_services(6)
        self.url: str = self.live_server_url+reverse('author:services')
        self.browser: ChromeBrowser = ChromeBrowser(self.url)
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def enter_into_services(self) -> None:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/nav/ul/li[1]/nav/ul/li[5]/a',
        ).click()

    def get_dashboard(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section',
        )

    def get_service(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/section/section/div[1]/div/a/span',
        )

    def get_service_title(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '//*[@id="id_title"]',
        )

    def get_service_description(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '//*[@id="id_description"]',
        )

    def get_form_data(self) -> WebElement:
        return self.browser.find_element_by_xpath(
            '/html/body/main/section/section/form',
        )

    def get_len_of_services_objects(self) -> int:
        return len(Service.objects.all())

    def test_services_load_correct_data(self) -> None:
        sign_in_with_selenium(self.browser)

        self.enter_into_services()

        self.assertEqual(
            self.get_len_of_services_objects(),
            6,
        )
        self.assertIn(
            'Service_Title',
            self.get_dashboard().text,
        )

    def test_service_edit_save_data_after_modification(self) -> None:
        sign_in_with_selenium(self.browser)
        self.enter_into_services()

        service: WebElement = self.get_service()
        service.click()

        new_title: str = 'This is the new title'
        service_title: WebElement = self.get_service_title()
        service_title.clear()
        service_title.send_keys(new_title)

        self.get_form_data().submit()

        self.assertIn(
            new_title,
            self.get_service_title().get_attribute('value'),
        )
        self.assertIn(
            'Salvo com sucesso',
            self.get_dashboard().text,
        )

    def test_services_not_allowed_to_save_without_data(self) -> None:
        sign_in_with_selenium(self.browser)
        self.enter_into_services()

        self.get_service().click()

        service_title: WebElement = self.get_service_title()
        service_title.clear()

        self.get_form_data().submit()

        self.assertIn(
            'Este campo é obrigatório.',
            self.get_form_data().text,
        )

    def test_services_delete_service_is_ok(self) -> None:
        sign_in_with_selenium(self.browser)
        self.enter_into_services()

        button_delete: WebElement = self.browser.find_element_by_xpath(
            '/html/body/main/section/section/' +
            'section/div[1]/div/span/form/button/span',
        )
        button_delete.click()

        Alert(self.browser.webdriver).accept()

        self.assertIn(
            'Serviço deletado com sucesso',
            self.get_dashboard().text,
        )
        self.assertEqual(
            self.get_len_of_services_objects(),
            5,
        )

    def test_services_create_new_service(self) -> None:
        sign_in_with_selenium(self.browser)
        self.enter_into_services()

        # button new service
        self.browser.find_element_by_xpath(
            '/html/body/main/section/section/div/a[1]/input',
        ).click()

        title: str = 'New Title'
        self.get_service_title().send_keys(title)

        self.get_service_description().send_keys(
            'This is the description'
        )

        self.get_form_data().submit()

        self.assertIn(
            'Salvo com sucesso',
            self.get_dashboard().text,
        )
        self.assertIn(
            title,
            self.get_dashboard().text,
        )
        self.assertEqual(
            self.get_len_of_services_objects(),
            7,
        )
