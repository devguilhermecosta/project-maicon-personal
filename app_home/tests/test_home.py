from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from app_home import views


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
