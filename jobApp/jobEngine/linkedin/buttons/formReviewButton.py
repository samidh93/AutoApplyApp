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

class FormReviewButtonHandler():
    def __init__(self) -> None:
        pass


    def _detectReviewButtonForm(self, form: WebElement):
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Review']")
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Review button element not found.")
            return False

    def _clickReviewPage(self, form: WebElement):
        # click the review page button
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Review']")
            # Click the button
            button.click()
            self.ReviewClicked = True
            return True
        except :
            # Handle the case when 'select' element is not found
            print("Review button element not found.")
            self.ReviewClicked = False
            return False

    def _execute_review(self, form:WebElement):
        current_header = self._find_header(form)
        # click review, if header is same, try filling the page if is not filled
        self._clickReviewPage(form)
        last_header = self._find_header(form)
        if last_header != current_header:
            # we skipped page
            return
            # on page review execute
        self.fillFormPage()
        # return button clicker
        return self._clickReviewPage(form)