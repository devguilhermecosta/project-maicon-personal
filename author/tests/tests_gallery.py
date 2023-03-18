from django.urls import reverse
from django.http import HttpResponse
from . author_base_test import AuthorTestBase


class GalleryTests(AuthorTestBase):
    def test_gallery_url_is_correct(self) -> None:
        response: str = reverse('author:gallery')

        self.assertEqual(response,
                         '/author/dashboard/gallery/',
                         )

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
        self.fail('Continuer from here')
