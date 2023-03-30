from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pathlib import Path
import sys
import os


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


class ImproperlyConfigured(BaseException):
    def __init__(self, message: str) -> None:
        self.message: str = message

    def __str__(self) -> str:
        return self.message


class ChromeBrowser:
    def __init__(self, url, *options) -> None:
        self.__browser: WebDriver = self.__make_chrome_browser(*options)
        try:
            self.__browser.get(url)
        except Exception as error:
            raise ImproperlyConfigured(
                f'Check url settings: {error}'
            )

    @property
    def webdriver(self) -> WebDriver:
        return self.__browser

    def __make_chrome_browser(self, *options) -> WebDriver:
        chrome_options: ChromeOptions = ChromeOptions()

        for option in options:
            chrome_options.add_argument(option)

        if os.environ.get('SELENIUM_HEADLESS') == '0':
            chrome_options.add_argument('--headless')

        try:
            chrome_service: Service = Service(
                executable_path=CHROMEDRIVER_PATH,
                )
        except Exception as error:
            raise ImproperlyConfigured(
                f'Check chromedriver version - {error}'
            )

        browser: Chrome = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options,
            )

        return browser

    def find_element_by_id(self, id: str) -> WebElement:
        return self.__browser.find_element(
            By.ID,
            id,
        )

    def find_element_by_xpath(self, xpath: str) -> WebElement:
        return self.__browser.find_element(
            By.XPATH,
            xpath,
        )

    def quit(self) -> None:
        return self.__browser.quit()


if __name__ == '__main__':
    from time import sleep
    browser = ChromeBrowser('https://www.google.com')
    sleep(2)
    browser.quit()
