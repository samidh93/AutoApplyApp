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

class FormNextButtonHandler():
    def __init__(self) -> None:
        pass

    def _detectNextButtonForm(self, form: WebElement):
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Next']")
            return True
        except :            
            # Handle the case when 'next' element is not found
            print("next button element not found.")
            return False

    def _clickNextPage(self, form: WebElement):
        # click the next page button
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Next']")
            # Click the button
            button.click()
            self.nextClicked = True
            return True
        except :
            # Handle the case when 'select' element is not found
            print("next button element not found.")
            self.nextClicked = False
            return False

    def _execute_next(self, form:WebElement): # this 90% of the cases 
        current_header = self._find_header(form)
        # click review, if header is same, try filling the page if is not filled
        self._clickNextPage(form)
        last_header = self._find_header(form)
        if last_header != current_header:
            # we skipped page
            return
        # on page next execute
        self.fillFormPage()
        # return button clicker
        return self._clickNextPage(form)


