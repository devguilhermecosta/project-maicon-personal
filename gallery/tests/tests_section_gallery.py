from django.test import TestCase, override_settings
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from django.core.paginator import Paginator

from gallery.views import Gallery
from gallery.models import Image

from .gallery_base_test import make_gallery_image, make_range_of_images

import contextlib
import shutil


TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=TEST_DIR + '/media')
class SectionGalleryTests(TestCase):
    def tearDown(self) -> None:
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def make_reverser(self) -> str:
        return reverse('gallery:gallery')

    def make_get_request(self) -> HttpResponse:
        return self.client.get(
            self.make_reverser(),
        )

    def test_gallery_url_is_correct(self) -> None:
        url: str = self.make_reverser()

        self.assertEqual(
            url,
            '/gallery/'
        )

    def test_gallery_view_is_correct(self) -> None:
        response: ResolverMatch = resolve(
            self.make_reverser(),
        )

        self.assertEqual(
            response.func.view_class,
            Gallery,
        )

    def test_gallery_status_code_200(self) -> None:
        response: HttpResponse = self.make_get_request()

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_gallery_return_no_images_found_if_no_images(self) -> None:
        response: HttpResponse = self.make_get_request()

        response_content: str = response.content.decode('utf-8')

        self.assertIn(
            'no images found',
            response_content,
        )

    def test_gallery_load_correct_images(self) -> None:
        make_gallery_image()
        response: HttpResponse = self.make_get_request()

        response_content: str = response.content.decode('utf-8')

        self.assertEqual(
            len(Image.objects.all()),
            1,
        )
        self.assertIn(
            'title image',
            response_content,
        )

    def test_gallery_is_paginated(self) -> None:
        make_range_of_images(11)

        response: HttpResponse = self.make_get_request()

        image: Image = response.context['objects']
        paginator: Paginator = image.paginator

        self.assertEqual(
            paginator.num_pages,
            2,
        )
