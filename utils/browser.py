from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import sys
import os


class ImproperlyConfigured(BaseException):
    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self) -> str:
        return self.message


ROOT_PATH = Path(__file__).parent.parent

WEBDRIVER_NAME: dict = {
    'windows': 'chromedriver_windows.exe',
    'ubuntu': 'chromedriver_ubuntu',
}
SYSTEM = sys.platform

if SYSTEM == 'win32':
    CHROMEDRIVER_PATH = str(
        ROOT_PATH / 'bin' / WEBDRIVER_NAME['windows']
    )
elif SYSTEM == 'linux':
    CHROMEDRIVER_PATH = str(
        ROOT_PATH / 'bin' / WEBDRIVER_NAME['ubuntu']
    )


def make_chrome_browser(*options) -> WebDriver:
    chrome_options: ChromeOptions = ChromeOptions()

    for option in options:
        chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '0':
        chrome_options.add_argument('--headless')

    try:
        chrome_service: Service = Service(executable_path=CHROMEDRIVER_PATH)
    except Exception as error:
        raise ImproperlyConfigured(
            f'Check chromedriver version - {error}'
        )

    browser: Chrome = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options,
        )

    return browser


if __name__ == '__main__':
    from time import sleep

    browser = make_chrome_browser()
    browser.get('https://www.google.com')
    sleep(2)
    browser.quit()
