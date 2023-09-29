from abc import ABC, abstractmethod
from selenium import webdriver
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
from googletrans import Translator

# Abstract base class for headers
class Header(ABC):
    @abstractmethod
    def detect(self, form:WebElement):
        pass
    
    @abstractmethod
    def fill(self, data):
        pass

# Concrete header classes
class ContactInfoHeader(Header):
    header = "Contact info"
    def detect(self, form:WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                return True
        except:
            print(f"no {self.header} header found")
            return False
    
    def fill(self, data):
        # Logic to fill in Contact Info data
        pass

class ResumeHeader(Header):
    header = "Resume"
    def detect(self, form:WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                return True
        except:
            print(f"no {self.header} header found")
            return False
    
    def fill(self, data):
        # Logic to fill in Upload Documents data
        pass

class AdditionalQuestionsHeader(Header):
    header = "Additional Questions"
    def detect(self, form:WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                return True
        except:
            print(f"no {self.header} header found")
            return False
    
    def fill(self, data):
        # Logic to fill in Additional Info data
        pass

class UnkownHeader(Header):
    def detect(self, form:WebElement):
        # Logic to detect the Additional Info header's web element
        pass
    
    def fill(self, data):
        # Logic to fill in Additional Info data
        pass




# Factory for creating headers
class HeaderFactory:
    def create_header(self, form:WebElement):
        headers = [ContactInfoHeader(), ResumeHeader(), AdditionalQuestionsHeader()]
        for header in headers:
            if header.detect(form):
                return header
        return UnkownHeader()
        raise ValueError("No header detected")




