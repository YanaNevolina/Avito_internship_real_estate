import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestAvitoVerticals:
    def setup_method(self, method):
        chrome_options = self.create_device_emulation_options("iPhone X")
        self.driver = webdriver.Chrome(options=chrome_options)

    def teardown_method(self, method):
        self.driver.quit()

    def test_metro_search_filter(self):
        self.open_home()

        self.open_search_settings()
        self.open_station_selector()

        self.select_station()
        self.select_lines_tab()

        self.check_no_expanded_lines()

        self.click_line()

        self.check_station_is_selected_in_line()
        self.check_apply_button_visible()

    def open_home(self):
        self.driver.get("https://m.avito.ru/")

    def open_search_settings(self):
        self.driver.find_element(By.XPATH, "//div[@data-marker=\'search-bar/filter\']").click()

    def open_station_selector(self):
        self.driver.find_element(By.XPATH, "//div[@data-marker=\'metro-select/withoutValue\']").click()

    def select_station(self):
        self.driver.find_element(By.CSS_SELECTOR, "#modalPage > div:nth-child(2) > div > div.css-1nm6007 > label:nth-child(1)").click()

    def select_lines_tab(self):
        self.driver.find_element(By.XPATH, "//button[@value=\'lines\']").click()

    def click_line(self):
        self.driver.find_element(By.XPATH, "//div[5]/div/button/span").click()

    def check_no_expanded_lines(self):
        elements = self.driver.find_elements(
            By.XPATH,
            "//div[contains(concat(\' \',normalize-space(@data-marker),\' \'),\'metro-select-dialog/lines/expanded\')]")
        assert len(elements) == 0

    def check_one_line_expanded(self):
        elements = self.driver.find_elements(
            By.XPATH,
            "//div[contains(concat(\' \',normalize-space(@data-marker),\' \'),\'metro-select-dialog/lines/expanded\')]")
        assert len(elements) == 1

    def check_station_is_selected_in_line(self):
        station_element = self.driver.find_element(By.XPATH, "//*[@id=\"modalPage\"]/div[2]/div/div[5]/div[5]/div[2]/ul/li[6]/label/input")
        assert station_element.is_selected() is True

    def check_apply_button_visible(self):
        elements = self.driver.find_elements(By.XPATH, "//*[@data-marker=\"metro-select-dialog/apply\"]")
        assert len(elements) == 1

    @staticmethod
    def create_device_emulation_options(device_name: str):
        mobile_emulation = {"deviceName": device_name}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        return chrome_options
