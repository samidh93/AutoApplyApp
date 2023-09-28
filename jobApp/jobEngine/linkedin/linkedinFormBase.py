from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import csv
import time
from ..user.candidateProfile import CandidateProfile
from collections.abc import Iterable


class LinkedinFormBase:
    def __init__(self) -> None:
        pass

    def _find_input_options_tag(self, element: WebElement, label=None):
        try:
            # Attempt to find the 'input' element inside the 'div' element
            input_elements = element.find_elements(By.TAG_NAME, 'input')
            # print(f"Input Value: {value}")
            return input_elements
        except NoSuchElementException:
            # Handle the case when 'input' element is not found
            print("Input elements not found.")

    def _find_label_tag(self, element: WebElement):
        try:
            label_element = element.find_element(By.TAG_NAME, 'label')
            label = label_element.text.strip()
            return label
            # print(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            print("no label element not found.")

    def _find_input_tag(self, element: WebElement, label=None):
        try:
            # Attempt to find the 'input' element inside the 'div' element
            input_element = element.find_element(By.TAG_NAME, 'input')
            value = input_element.get_attribute('value').strip()
            # print(f"Input Value: {value}")
            return input_element
        except NoSuchElementException:
            # Handle the case when 'input' element is not found
            print("Input element not found.")

    def _find_select_tag(self, element: WebElement, label=None):
        try:
            # Attempt to find the 'select' element inside the 'div' element
            select_element = element.find_element(By.TAG_NAME, 'select')
            # Create a Select object
            select = Select(select_element)
            # assign label with select element object
            selected_option = select.options
            return select_element
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            print("Select element not found.")
