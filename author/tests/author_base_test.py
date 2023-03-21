from django.test import TestCase
from django.contrib.auth.models import User
from gallery.models import Image
from app_home.tests.home_base_test import make_simple_image


class AuthorTestBase(TestCase):
    def make_login(self) -> bool:
        user_data: dict = {
            'username': 'username',
            'password': 'password'
        }

        User.objects.create_user(
            **user_data
        )

        return self.client.login(
            **user_data
            )


def create_user(**kwargs) -> User:
    """
    Optional param: username: str,
    Optional param: password: str
    """
    user: User = User.objects.create_user(
        username=kwargs.pop('username', 'username'),
        password=kwargs.pop('password', 'password'),
    )

    return user


def make_image_object(**kwargs) -> Image:
    """
    Optional param: title: str,
    Optional param: description: str
    """
    image: Image = Image.objects.create(
        title=kwargs.pop('title', 'title'),
        description=kwargs.pop('description', 'description'),
        cover=make_simple_image(),
    )

    return image
