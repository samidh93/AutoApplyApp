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
from .linkedinFormBaseElemFinder import LinkedinFormBaseFinder
''' handle linkedin easy apply form Contact info'''

class FormSubmitButtonHandler():
    def __init__(self) -> None:
        pass

    def _clickSubmitPage(self, form: WebElement):
        # click the submit page button
        # Find the button using its aria-label attribute
        try:
            wait = WebDriverWait(self.driver, 1)
            button:WebElement = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit application']")))
            # Scroll to the button to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            button.click()
            self.SubmitClicked = True
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Submit button element not found.")
            self.SubmitClicked = False
            return False
    def _detectSubmitButtonForm(self, form: WebElement):
        # Find the button using its aria-label attribute
        try:
            #button = form.find_element(By.XPATH, "//span[text()='Submit application']")
            # Wait for the button to be clickable or visible
            wait = WebDriverWait(self.driver, 1)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit application']")))
            # Scroll to the button to ensure it's in view
            self.driver.execute_script("arguments[0].scrollIntoView();", button)
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Submit button element not found.")
            return False

    def _execute_submit(self, form:WebElement):
        # on page submit execute
        return self._clickSubmitPage(form)