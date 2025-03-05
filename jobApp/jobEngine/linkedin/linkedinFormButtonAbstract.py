from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import csv
import time
from ..user.candidateProfile import CandidateProfile
from collections.abc import Iterable
from .linkedinFormHeaderAbstract import HeaderFactory
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading
# Abstract base class for buttons
import logging
logger = logging.getLogger(__name__)

class Button(ABC):
    submitted = False
    reviewed = False

    @abstractmethod
    def detect(self, form, driver):
        pass

    @abstractmethod
    def click(self):
        pass

    def fillSection(self, form):
        try:
            headerfactory = HeaderFactory()
            header = headerfactory.create_header(form)
            header.fill(form=form, data=self.data)
        except:
            logger.info("error filling section header")

    def set_data(self, data):
        self.data = data

# Concrete button classes


class SubmitButton(Button):
    button_name = "Submit"

    def detect(self, form: WebElement, driver):
        # Find the button using its aria-label attribute
        try:
            self.form = form
            self.driver = driver
            script = """
            let submitButton = document.querySelector("button[aria-label='Submit application']");
            return submitButton;
            """
            self.button = driver.execute_script(script)
            if self.button:
                logger.info("submit button found")
                return True
            else:
                logger.info("Submit button not found.")
                return False
        except:
            logger.info("Submit button element not found on form ")
            return False

    def click(self):
        # click the submit page button
        try:
            self.button.click()
            logger.info(f"button {self.button_name} clicked")
            self.SubmitClicked = True
            self.submitted = True
            return True
        except:
            # Handle the case when 'select' element is not found
            logger.info("Submit button element not clicked.")
            self.SubmitClicked = False
            return False


class ReviewButton(Button):
    button_name = "Review"

    def detect(self, form: WebElement, driver):
        # Find the button using its aria-label attribute
        try:
            self.button = form.find_element(By.XPATH,  "//span[text()='Review']")
            logger.info("page form with review detected")
            self.driver = driver
            return True
        except:
            # Handle the case when 'next' element is not found
            logger.info("Review button element not found.")
            return False

    def click(self):
        # Logic to click the Review button
        try:
            self.button.click()
            logger.info(f"button {self.button_name} clicked")
            self.ReviewClicked = True
            self.reviewed = True
            return True
        except:
            # Handle the case when 'select' element is not found
            logger.info("Review button element not found.")
            self.ReviewClicked = False
            return False


class NextButton(Button):
    button_name = "Next"

    def detect(self, form: WebElement, driver: webdriver.Chrome):
        # Find the button using its aria-label attribute
        try:
            self.button = form.find_element(By.XPATH, "//span[text()='Next']")
            logger.info("page form with next detected")
            self.driver = driver
            return True
        except:
            # Handle the case when 'next' element is not found
            logger.info("next button element not found.")
            return False

    def click(self):
        # Logic to click the Next button
        try:
            self.button.click()
            logger.info(f"button {self.button_name} clicked")
            self.nextClicked = True
            return True
        except:
            # Handle the case when 'select' element is not found
            logger.info("next button element not found.")
            self.nextClicked = False
            return False


class ButtonFactory:
    def create_button(self, form: WebElement, driver: webdriver, data: CandidateProfile):
        buttons: [Button] = [SubmitButton(), ReviewButton(), NextButton()]

        def create_button_task(button: Button):
            try:
                if button.detect(form, driver):
                    button.set_data(data)
                    return button
            except:
                logger.info("error when detecting button")
            return None

        for button in buttons:
            butt= create_button_task(button=button)
            # Raise an exception if no button is detected
            if butt != None:
                return butt
        
        raise ValueError("No button detected")
