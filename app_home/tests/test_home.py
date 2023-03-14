from django.test import TestCase, override_settings
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from app_home import views
from app_home import models as md
from .home_base_test import (
    make_social_network,
    make_section_intro,
    make_profle,
    make_pre_gallery,
    make_adress,
    make_queryset_services,
    )
import contextlib
import shutil


TEST_DIR = 'test_data'


# modify the upload location of media files
@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class HomeTests(TestCase):
    def tearDown(self) -> None:
        # delete the new location of media files after the tests
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def test_home_url_is_correct(self) -> None:
        url: str = reverse('home:home')

        self.assertEqual(url, '/home/')

    def test_home_load_correct_view(self) -> None:
        url: str = reverse('home:home')
        response: ResolverMatch = resolve(url)

        self.assertEqual(response.func.view_class, views.HomeView)

    def test_home_load_correct_template(self) -> None:
        url: str = reverse('home:home')
        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'app_home/pages/home.html')

    def test_home_status_code_200_ok(self) -> None:
        response: HttpResponse = self.client.get(
            reverse('home:home')
        )

        self.assertEqual(response.status_code, 200)

    def test_home_load_correct_content(self) -> None:
        home_data: dict = {
            'social_network': make_social_network(),
            'section_intro': make_section_intro(),
            'profile': make_profle(),
            'pre_gallery': make_pre_gallery(),
            'adress': make_adress(),
        }

        home_content: md.HomeContent = md.HomeContent.objects.create(
            **home_data,
        )

        # set the services because the relationship is many-to-many
        home_content.services.set(
            make_queryset_services(2)
            )
        response: HttpResponse = self.client.get(
            reverse('home:home')
        )

        response_content: str = response.content.decode('utf-8')

        self.assertIn('instagram_link', response_content)
        self.assertIn('whatsapp_phone', response_content)
        self.assertIn('section_intro_title', response_content)
        self.assertIn('section_intro_description', response_content)
        self.assertIn('profile_title', response_content)
        self.assertIn('profile_description', response_content)
        self.assertIn('pre_gallery_title', response_content)
        self.assertIn('pre_gallery_description', response_content)
        self.assertIn('adress_name', response_content)
        self.assertIn('adress_city', response_content)
        self.assertIn('service_title', response_content)
        self.assertIn('service_description', response_content)
