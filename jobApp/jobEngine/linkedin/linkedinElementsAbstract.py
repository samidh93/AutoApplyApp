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
import logging
logger = logging.getLogger(__name__)

class Element(ABC):
    @abstractmethod
    def find(self, element: WebElement):
        pass


class LabelElement(Element):
    def find(self, element: WebElement):
        try:
            label_element = element.find_element(By.TAG_NAME, 'label')
            labelText = label_element.text.strip()
            logger.info("label: %s", labelText)
            return label_element
        except NoSuchElementException:
            logger.info("no label element not found.")

    def handle(self, div:WebElement, element: WebElement):
        label_elements_map = {}
        inputObj = InputElement()
        selectObj = SelectElement()
        textAreaObj = TextAreaElement()
        try:
            input_elem = inputObj.find(div)
            if input_elem is not None:
                logger.info(f"added input element with label: {element.text}")
                label_elements_map[element] = input_elem
        except:
            try:
                textarea_elem = textAreaObj.find(div)
                if textarea_elem is not None:
                    logger.info(f"added text element with label: {element.text}")
                    label_elements_map[element] = textarea_elem
            except:
                select_elem = selectObj.find(div)
                if select_elem is not None:
                    logger.info(f"added select element with label: {element.text}")
                    label_elements_map[element] = select_elem
        return label_elements_map

class InputElement(Element):
    def find(self, element: WebElement):
        try:
            # Attempt to find the 'input' element inside the 'element' element
            input_element = element.find_element(By.TAG_NAME, 'input')
            value = input_element.get_attribute('value').strip()
            logger.info("input value: %s", value)
            return input_element
        except NoSuchElementException:
            logger.info("Input element not found.")
            raise

class TextAreaElement(Element):
    def find(self, element: WebElement):
        try:
            # Attempt to find the 'TextArea' element inside the 'element' element
            TextArea_element = element.find_element(By.TAG_NAME, 'textarea')
            value = TextArea_element.get_attribute('value').strip()
            logger.info("TextArea value: %s", value)
            return TextArea_element
        except NoSuchElementException:
            logger.info("TextArea element not found.")
            raise

class InputOptionsElements(Element):
    def find(self, element: WebElement):
        try:
            # Attempt to find the 'input' element inside the 'element' element
            input_elements = element.find_elements(By.TAG_NAME, 'input')
            #value = input_element.get_attribute('value').strip()
            return input_elements
        except NoSuchElementException:
            logger.info("Input element not found.")

class CheckboxOptionsElements(Element):
    def find(self, element: WebElement):
        try:
            # Attempt to find the 'input' element inside the 'element' element
            checkbox_elements = element.find_elements(By.CSS_SELECTOR, '[data-test-text-selectable-option]')
            #value = checkbox_element.get_attribute('value').strip()
            return checkbox_elements
        except NoSuchElementException:
            logger.info("options element not found.")

class FieldsetElement(Element):
    def find(self, element: WebElement):
        try:
            fieldset_element = element.find_element(By.TAG_NAME, 'fieldset')
            logger.info(f"Fieldset: {fieldset_element.text}")
            return fieldset_element
            # logger.info(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            logger.info("fieldset element not found.")

    def handle(self, element: WebElement):
        label_elements_map = {}
        legend = SpanElement()
        inputs = CheckboxOptionsElements()
        try:
            # we have a set of fields (dialog or checkbox)
            # get the question as text
            legend_text: WebElement = legend.find(element) 
            # we have list of options, we collect them
            elems = inputs.find(
                element)
            label_elements_map [legend_text]= elems
            return label_elements_map
        except:
            logger.info("cant handle Fieldset")
            return label_elements_map


class SpanElement(Element):
    def find(self, element: WebElement):
        try:
            span_element = element.find_element(By.TAG_NAME, 'legend')
            logger.info("span text:", span_element.text.strip())
            return span_element
            # logger.info(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            logger.info("no span element found.")


class SelectElement(Element):
    def find(self, element: WebElement):
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
            logger.info("Select element not found.")
