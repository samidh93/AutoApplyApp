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


class Element(ABC):
    @abstractmethod
    def find(self, element: WebElement):
        pass


class LabelElement(Element):
    def find(self, element: WebElement):
        try:
            label_element = element.find_element(By.TAG_NAME, 'label')
            labelText = label_element.text.strip()
            print("label:", labelText)
            return label_element
        except NoSuchElementException:
            print("no label element not found.")

    def handle(self, div:WebElement, element: WebElement):
        label_elements_map = {}
        inputObj = InputElement()
        selectObj = SelectElement()
        try:
            input_elem = inputObj.find(div)
            # text field
            if input_elem is not None:
                print(f"added input element with label: {element.text}")
                label_elements_map[element] = input_elem
                # search for select options
            else:
                select_elem = selectObj.find(div)
                if select_elem is not None:
                    print(f"added select element with label: {element.text}")
                    label_elements_map[element] = select_elem
        except:
            print("input element not handled")
        return label_elements_map

class InputElement(Element):
    def find(self, element: WebElement):
        try:
            # Attempt to find the 'input' element inside the 'element' element
            input_element = element.find_element(By.TAG_NAME, 'input')
            value = input_element.get_attribute('value').strip()
            print("input value: ", value)
            return input_element
        except NoSuchElementException:
            print("Input element not found.")

class InputOptionsElements(Element):
    def find(self, element: WebElement):
        try:
            # Attempt to find the 'input' element inside the 'element' element
            input_element = element.find_element(By.TAG_NAME, 'input')
            value = input_element.get_attribute('value').strip()
            return input_element
        except NoSuchElementException:
            print("Input element not found.")


class FieldsetElement(Element):
    def find(self, element: WebElement):
        try:
            fieldset_element = element.find_element(By.TAG_NAME, 'fieldset')
            print(f"Fieldset: {fieldset_element.text}")
            return fieldset_element
            # print(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            print("fieldset element not found.")

    def handle(self, element: WebElement):
        label_elements_map = {}
        try:
            # we have a set of fields (dialog or checkbox)
            span_text: WebElement = SpanElement.find(element)
            inputs_elems = InputOptionsElements.find(
                element, span_text.text)
            label_elements_map [span_text.text]= inputs_elems
            return label_elements_map
        except:
            print("cant handle Fieldset")
            return label_elements_map


class SpanElement(Element):
    def find(self, element: WebElement):
        try:
            span_element = element.find_element(By.TAG_NAME, 'span')
            print("span text:", span_element.text.strip())
            return span_element
            # print(f"Label: {label}")
        except NoSuchElementException:
            # Handle the case when 'select' element is not found
            print("no span element found.")


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
            print("Select element not found.")
