"""
Test task for Wisebits by Druzhinin Daniil
"""

import time
import allure
import pytest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from base import helper

USERNAME = helper.make_username()
PASSWORD = 'test12345'
EMAIL = helper.make_email()
START_URL = 'https://livexp.dev'

capabilities = {
    "browserName": "chrome",
    "browserVersion": "84.0",
    "selenoid:options": {
        "enableVNC": True,
        "enableVideo": False
    }
}


class TestWB:
    def setup(self) -> None:
        self.browser = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub", desired_capabilities=capabilities)
        self.browser.get(START_URL)
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 10)
        time.sleep(3)

    def teardown(self) -> None:
        self.browser.quit()

    @allure.epic('Live XP')
    @allure.feature('Sign Up')
    @allure.testcase('usr success sign up')
    def test_all_rows(self):
        """
        Sign up and check user
        """
        signup_button = self.browser.find_element_by_xpath("//span[contains(text(),'Sign up')]")
        signup_button.click()
        time.sleep(3)


        username_input = self.browser.find_element_by_xpath("//input[@name='login']")
        email_input = self.browser.find_element_by_xpath("//input[@name='email']")
        password_input = self.browser.find_element_by_xpath("//input[@name='password']")

        username_input.send_keys(USERNAME)
        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)

        signin_button = self.browser.find_element_by_xpath(
            "//button[@type='submit']/span[contains(text(),'Sign up')]")
        signin_button.click()
        time.sleep(3)


if __name__ == "__main__":
    pytest.main()
