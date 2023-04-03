from app_home.tests.home_base_test import make_simple_image
from gallery.models import Image


def make_gallery_image() -> Image:
    data: dict = {
        'title': 'title image',
        'description': 'description image',
        'cover': make_simple_image(),
    }

    image_obj: Image = Image.objects.create(
        **data,
    )

    return image_obj


def make_range_of_images(num_of_images: int) -> None:
    for i in range(num_of_images):
        make_gallery_image()
