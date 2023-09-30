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
from .linkedinElementsAbstract import LabelElement, InputElement, FieldsetElement, SpanElement, SelectElement
from .linkedinFunctions import LinkedinUtils
# Abstract base class for Divss


class Divs(ABC):
    @abstractmethod
    def find(self, form: WebElement):
        pass

    @abstractmethod
    def createDictFromDivs(self, divs):
        pass

# Concrete Divs classes


class DivsSelectionGrouping(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(
                By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
            print("found divs with selection grouping")
            if divs != None:
                return divs
        except NoSuchElementException:
            print("No div selection grouping elements found")

    def createDictFromDivs(self, divs):
        # Iterate over the divs and extract the label and corresponding input/select values
        label_elements_map = {}
        field = FieldsetElement()
        label = LabelElement()
        for div in divs:
            try:
                print("processing form fields")
                fieldset = field.find(div)
                if fieldset is not None:
                    label_elements_map.update(field.handle(fieldset))
                else:
                    labelElem = label.find(div)
                    if labelElem is not None:
                        label_elements_map.update(label.handle(div, labelElem))
            except:
                continue
        return label_elements_map
    
    def send_user_contact_infos(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        googleTranslator = Translator()
        for label, element in elements_dict.items():
            try:
                if googleTranslator.translate(label.text, dest='en').text == 'First name':
                    LinkedinUtils.send_value(element, user.firstname)
                    print(f"firstname to send: {user.firstname}")
                elif googleTranslator.translate(label.text, dest='en').text == 'Last name':
                    LinkedinUtils.send_value(element, user.lastname)
                    print(f"lastname to send: {user.lastname}")
                elif googleTranslator.translate(label.text.split('\n', 1)[0], dest='en').text == 'Phone country code':
                    print("selecting user phone country code: ", user.phone_code)
                    LinkedinUtils.select_option(element, user.phone_code)
                elif googleTranslator.translate(label.text, dest='en').text == 'Mobile phone number':
                    LinkedinUtils.send_value(element, user.phone_number)
                    print(f"mobile to send: {user.phone_number}")
                elif googleTranslator.translate(label.text.split('\n', 1)[0], dest='en').text == 'Email address':
                    print(f"selecting user email: {user.email}")
                    LinkedinUtils.select_option(element, user.email)
                else:
                    raise ValueError("Unsupported label: {}".format(label))
            except:
                continue

# Concrete Divs classes

class DivsDocumentUpload(Divs):
    def find(self, form: WebElement):
        try:
            div_elements = form.find_elements(
                By.XPATH, "//div[contains(@class, 'js-jobs-document-upload__container') and contains(@class, 'display-flex') and contains(@class, 'flex-wrap')]")
            if div_elements != None:
                return div_elements

        except NoSuchElementException:
            print("No upload elements found")
            return False

    def createDictFromDivs(self, divs):
        # Iterate over the divs and extract the label and corresponding input/select values
        label_elements_map = {}
        try:
            for div in divs:  # list of divs
                # Div contains label and inpout tag
                label = LabelElement().find(div)
                if label is not None:
                    input_elem = InputElement().find(div)
                    # text field
                    if input_elem is not None:
                        print(f"added input element with label: {label}")
                        label_elements_map[label] = input_elem
            return label_elements_map
        except Exception as E:
            print("create dict from divs doc upload error: ", str(E))
            return {}

    def send_user_documents(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        googleTranslator = Translator()
        for label, element in elements_dict.items():
            if googleTranslator.translate(label.text, dest='en').text == 'Upload resume':
                LinkedinUtils.send_value(element, user.resume)
            elif googleTranslator.translate(label.text, dest='en').text == "Upload cover letter":
                pass
            else:
                raise ValueError("Unsupported label: {}".format(label))
