from django.test import override_settings
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from . author_base_test import AuthorTestBase
from author.views import GalleryImageView
from gallery.models import Image
from app_home.tests.home_base_test import make_simple_image
import shutil
import contextlib


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
        self.fail(
            'Ver o que fica mais fácil: \n'
            '1 - criar um teste normal para editar e deletar images.\n'
            '2 - criar um test funcional.'
        )
