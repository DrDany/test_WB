"""
Test task for Wisebits by Druzhinin Daniil
"""

import unittest
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

NUMBER_OF_RECORDS_TO_CHECK = 6
NUMBER_OF_ALL_RECORDS = 91

START_URL = "https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all"
PATH = "screenshots"

try:
    os.mkdir(PATH)
except OSError:
    print(F"Directory {PATH} alredy exists")
else:
    print(F"Create directory {PATH}")

JS_SELECT = ("window.editor.getDoc().setValue""('select * from customers where city = \"London\"')")
JS_INSERT = (
    'window.editor.getDoc().setValue("INSERT INTO Customers (CustomerName, ContactName, Address, '
    "City, PostalCode, Country) VALUES ('Test', 'Test', 'Test', 'Test', 'Test', 'Test')\") "
)
JS_SELECT_INSERT = (
    "window.editor.getDoc().setValue "
    "(\"select * from Customers where CustomerName = 'Test'\")"
)
JS_UPDATE = (
    "window.editor.getDoc().setValue(\"update Customers set CustomerName = "
    "'Jonh',ContactName = 'Doe', Address = 'Street', "
    "City = 'City', PostalCode = '1234567',Country = 'USA' where CustomerID = 1\")"
)
JS_SELECT_UPDATE = (
    "window.editor.getDoc().setValue"
    "(\"select * from Customers where CustomerName = 'Jonh'\")"
)

capabilities = {
    "browserName": "chrome",
    "browserVersion": "84.0",
    "selenoid:options": {
        "enableVNC": True,
        "enableVideo": False
    }
}

class TestCheck(unittest.TestCase):
    """test class"""

    def setUp(self) -> None:
        self.browser = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub", desired_capabilities=capabilities)
        self.browser.get(START_URL)
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 10)

    def test_all_rows(self):
        """
        select all rows from Customer compare amount of rows
        and check row with ContactName is CGiovanni Rovelli has address Via Ludovico il Moro 22
        """
        self.browser.execute_script(
            "window.editor.getDoc().setValue('select * from customers')"
        )
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "w3-green")))
        self.browser.find_element_by_class_name("w3-green").click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Number of Records:')]")
            )
        )
        number_of_table_records = self.browser.find_element_by_xpath(
            "//div[contains(text(),'Number of Records:')]"
        ).text
        amount_of_result_string = int(
            number_of_table_records.partition(":")[2]
        )
        self.browser.save_screenshot("screenshots/all_records.png")
        self.assertEqual(amount_of_result_string, NUMBER_OF_ALL_RECORDS,
                         F"amount of result aren't {NUMBER_OF_ALL_RECORDS}")
        self.wait.until(EC.visibility_of_element_located((By.ID, "divResultSQL")))

        try:
            tr_with_target_text = self.browser.find_element_by_id('divResultSQL') \
                .find_element_by_xpath("//td[contains(text(),'CGiovanni Rovelli')]")
            td_with_address = tr_with_target_text.find_element_by_xpath(
                "//td[contains(text(),'Via Ludovico il Moro 22')]")
            self.assertEqual(td_with_address.text, "Via Ludovico il Moro 22",
                             "address is not Via Ludovico il Moro 22")
        except NoSuchElementException:
            self.fail("Element with ContactName 'CGiovanni Rovelli' not found")

    def test_rows_where_city_is_london(self):
        """
        select rows where city is London and compare result have to be 6
        """
        self.browser.execute_script(JS_SELECT)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "w3-green")))
        self.browser.find_element_by_class_name("w3-green").click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Number of Records:')]")
            )
        )
        number_of_table_records = self.browser.find_element_by_xpath(
            "//div[contains(text(),'Number of Records:')]"
        ).text

        amount_of_result_string = int(
            number_of_table_records.partition(":")[2]
        )
        self.browser.save_screenshot("screenshots/London_select.png")
        self.assertEqual(
            amount_of_result_string,
            NUMBER_OF_RECORDS_TO_CHECK,
            F"amount of result aren't {NUMBER_OF_RECORDS_TO_CHECK}"
        )

    def test_insert_new_row(self):
        """
        insert row with value "Test" and select this row
        """
        self.browser.execute_script(JS_INSERT)
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "w3-green")))
        self.browser.find_element_by_class_name("w3-green").click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Rows affect')]")
            )
        )
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "w3-green")))
        self.browser.execute_script(JS_SELECT_INSERT)
        self.browser.find_element_by_class_name("w3-green").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "divResultSQL")))
        self.browser.save_screenshot("screenshots/insert_result.png")
        new_user = (
            self.browser.find_element_by_id("divResultSQL")
            .find_element_by_xpath("//td[contains(text(),'Test')]").text
        )
        self.assertEqual(new_user, "Test", "новый пользователь не добавлен")

    def test_update_row(self):
        """
        update row where customerID = 1 set CustomerName = Jonh and select this row
        """
        self.browser.execute_script(JS_UPDATE)
        self.browser.find_element_by_class_name("w3-green").click()
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Rows affect')]")
            )
        )
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "w3-green")))
        self.browser.execute_script(JS_SELECT_UPDATE)
        self.browser.find_element_by_class_name("w3-green").click()
        self.wait.until(EC.visibility_of_element_located((By.ID, "divResultSQL")))
        self.browser.save_screenshot("screenshots/update_result.png")
        update_user = (
            self.browser.find_element_by_id("divResultSQL")
            .find_element_by_xpath("//td[contains(text(),'Jonh')]").text
        )
        self.assertEqual(update_user, "Jonh", "Строка не обновилась")

    def tearDown(self) -> None:
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()
