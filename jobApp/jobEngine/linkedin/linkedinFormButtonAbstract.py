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

# Abstract base class for buttons
class Button(ABC):
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
            print("error filling section header")

    def set_data(self, data):
        self.data = data
    

# Concrete button classes
class SubmitButton(Button):
    button_name = "Submit"
    def detect(self, form: WebElement, driver):
        # Find the button using its aria-label attribute
        try:
            time.sleep(2)
            # Wait for the button to be clickable or visible
            self.button = form.find_element(By.XPATH,  "//span[text()='Submit application']")
            print("page form with submit detected")
            self.form = form
            self.driver = driver
            return True
        except:
            print("Submit button element not found" )
            return False
    
    def click(self):
        # click the submit page button
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", self.button)
            self.button.click()
            print(f"button {self.button_name} clicked")
            self.SubmitClicked = True
            return True
        except:
            # Handle the case when 'select' element is not found
            print("Submit button element not found.")
            self.SubmitClicked = False
            #return False
        else:
            self.form.submit()
            print("form submitted")
            self.SubmitClicked = True




class ReviewButton(Button):
    button_name = "Review"
    def detect(self, form: WebElement, driver):
        # Find the button using its aria-label attribute
        try:
            self.button = form.find_element(By.XPATH,  "//span[text()='Review']")
            print("page form with review detected")
            self.driver = driver
            return True
        except:
            # Handle the case when 'next' element is not found
            print("Review button element not found.")
            return False

    
    def click(self):
        # Logic to click the Review button
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", self.button)
            self.button.click()
            print(f"button {self.button_name} clicked")
            self.ReviewClicked = True
            return True
        except:
            # Handle the case when 'select' element is not found
            print("Review button element not found.")
            self.ReviewClicked = False
            return False

class NextButton(Button):
    button_name = "Next"

    def detect(self, form: WebElement, driver:webdriver.Chrome):
        # Find the button using its aria-label attribute
        try:
            self.button = form.find_element(By.XPATH, "//span[text()='Next']")
            print("page form with next detected")
            self.driver = driver
            return True
        except:
            # Handle the case when 'next' element is not found
            print("next button element not found.")
            return False

    
    def click(self):
        # Logic to click the Next button
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", self.button)
            self.button.click()
            print(f"button {self.button_name} clicked")
            self.nextClicked = True
            return True
        except :
            # Handle the case when 'select' element is not found
            print("next button element not found.")
            self.nextClicked = False
            return False


# Factory for creating buttons
class ButtonFactory:
    def create_button(self, form:WebElement, driver:webdriver, data:CandidateProfile):
        buttons: [Button] = [SubmitButton(), ReviewButton(), NextButton()]
        for button in buttons:
            if button.detect(form, driver):
                button.set_data(data)
                return button
        raise ValueError("No button detected")

