from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from app_home import views
from app_home.models import HomeContent


class HomeTests(TestCase):
    def test_home_url_is_correct(self) -> None:
        url: str = reverse('home:home')

        self.assertEqual(url, '/')

    def test_home_load_correct_view(self) -> None:
        url: str = reverse('home:home')
        response: ResolverMatch = resolve(url)

        self.assertEqual(response.func.view_class, views.HomeView)

    def test_home_load_correct_template(self) -> None:
        url: str = reverse('home:home')
        response: HttpResponse = self.client.get(url)

        self.assertTemplateUsed(response, 'app_home/pages/home.html')

    def test_home_contact_load_correct_data(self) -> None:
        data: dict = {
            'instagram_link': 'www.instagram.com',
            'facebook_link': 'www.facebook.com',
            'whatsapp_link': 'www.whatsapp.com',
            'instagram_text': '@instagram',
            'facebook_text': '@facebook',
            'whatsapp_phone': '(46)1234-5678',
        }

        HomeContent.objects.create(**data)
        
        response: HttpResponse = self.client.get(
            reverse('home:home')
        )

        response_content: str = response.content.decode('utf-8')

        self.assertIn(data['instagram_link'], response_content)
        self.assertIn(data['facebook_link'], response_content)
        self.assertIn(data['whatsapp_link'], response_content)
        self.assertIn(data['instagram_text'], response_content)
        self.assertIn(data['facebook_text'], response_content)
        self.assertIn(data['whatsapp_phone'], response_content)
        self.fail('testar o max_length e min_length')
