from django.test import TestCase
from django.contrib.auth.models import User
from gallery.models import Image
from app_home.tests.home_base_test import make_simple_image
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver


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


def sign_in_with_selenium(browser: WebDriver) -> None:
    input_user: WebElement = browser.find_element(
        By.XPATH,
        '//*[@id="id_username"]',
    )
    input_user.send_keys('username')

    input_password: WebElement = browser.find_element(
        By.XPATH,
        '//*[@id="id_password"]',
    )
    input_password.send_keys('password')

    button_submit: WebElement = browser.find_element(
        By.XPATH,
        '/html/body/main/section/form/button'
    )
    button_submit.click()


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
