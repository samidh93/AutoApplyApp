from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import csv
import time
from ...user.candidateProfile import CandidateProfile
from collections.abc import Iterable


class LinkedinFormBaseHandler:
    def __init__(self) -> None:
        pass

    def _handle_text_question(self, label, element: WebElement ):
        try:
            print("processing text question")
            if "salary" in label:
                self.send_value(element, self.candidate.salary)
            if "Erfahrung" or "Experience" in label:
                self.send_value(element, self.candidate.years_exp)
        except:
            pass 
    def _handle_dialog_question(self, label, element: WebElement ):
        try:
            print("processing dialog question")
            input_options = element.find_elements(By.TAG_NAME, "input")
            for opt in input_options:
                print("option: ", opt)
                if opt.get_attribute("value") == "Yes":
                    opt.click()
        except:
            pass 
    def _handle_select_question(self, label, element: WebElement ):
        try:
            print("processing select question")
            dropdown = Select(element)
            # Get the number of options in the dropdown
            options_count = len(dropdown.options)
            # Calculate the index of the middle option
            middle_index = options_count // 2
            # Select the option in the middle by index
            dropdown.select_by_index(options_count-1)
        except:
            pass 
    def _handle_checkbox_question(self, label , elements: WebElement):
        try:
            print("checkbox question")
            options_count = len(elements)
            middle_index = options_count // 2
            # random value in the middle
            checkbox = elements[options_count-1]
            # Find the associated label using its attributes (for or id) or relationship (preceding-sibling, following-sibling, etc.)
            label = checkbox.find_element(By.XPATH, "//label[@for='" + checkbox.get_attribute("id") + "']")
            if not label.is_selected():
                label.click()  # Click the label to interact with the checkbox
                print("Label clicked successfully.")
        except Exception as e:
            print("An error occurred:", e)