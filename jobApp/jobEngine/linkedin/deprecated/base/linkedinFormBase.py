from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import csv
import time
from ....user.candidateProfile import CandidateProfile
from collections.abc import Iterable
from .finder.linkedinFormBaseElemFinder import LinkedinFormBaseFinder


class LinkedinFormBase:
    def __init__(self) -> None:
        pass

    def send_value(self, element: WebElement, value: str):
        element_type = element.get_attribute("type")
        if element_type == "file":
            print(f"sending file path: {value}")
            element.send_keys(value)
        elif element_type == "text":
            element.clear()
            element.send_keys(value)
        else:
            print("input type not recognized")

    def click_option(self, element: WebElement, value: str):
        element_type = element.get_attribute("type")
        if element_type == "radio":
            for elem in element:
                if elem == value:
                    elem.click()
        elif element_type == "checkbox":
            for elem in element:
                if elem == value:
                    elem.click()

    def select_option(self, select_element, user_value):
        select = Select(select_element)
        if isinstance(select.options, Iterable):
            if user_value in select.options:
                select.select_by_visible_text(user_value)
            else:  # return first option to bypass error; needed to be corrected
                select.select_by_visible_text(
                    select.first_selected_option.accessible_name)
            return
        else:
            select.select_by_visible_text(select.first_selected_option.text)


    def _createDictFromFormDiv(self, divs:  list[WebElement]):
        # Iterate over the divs and extract the label and corresponding input/select values
        label_elements_map = {}
        for div in divs:
            fieldset = _find_fieldset_tag(div)
            if fieldset is not None:
                # we have a set of fields (dialog or checkbox)
                span_text = _find_span_text(fieldset)
                inputs_elems = _find_input_options_tag(fieldset, span_text.text)
                print(f"added field element with label: {span_text}")
                label_elements_map[span_text.text] = inputs_elems
            # search for label w
            else:
                label = _find_label_tag(div)
                if label is not None:
                    input_elem = _find_input_tag(div, label)
                    # text field
                    if input_elem is not None:
                        print(f"added input element with label: {label.text}")
                        label_elements_map[label] = input_elem
                    # search for select options
                    else:
                        select_elem = _find_select_tag(div, label)     
                        if select_elem is not None:
                            print(f"added select element with label: {label}")
                            label_elements_map[label] = select_elem
        return label_elements_map
