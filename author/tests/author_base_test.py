from django.test import TestCase
from django.contrib.auth.models import User


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
