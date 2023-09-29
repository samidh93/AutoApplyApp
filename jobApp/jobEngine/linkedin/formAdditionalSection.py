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

class FormAdditionalHandler():
    def __init__(self) -> None:
        pass

    def _fill_additionals(self, form: WebElement):
        #self._find_application_form()  # try to find the form
        try:
            divs = self._find_divs_selection_grouping()
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                self._createDictFromFormDiv(divs)
                # fill the form with candidate data
                self._send_user_answers(self.candidate, self.label_elements_map)
                # click next buttton
                self.label_elements_map.clear()
        except Exception as e:
            print("catched error while filling additional questions", e)

    def _send_user_answers(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        # try to answer most form questions
        for label, element in elements_dict.items():
            if isinstance(element, list):
                print("The element is of type list.")
                if element[0].get_attribute("type") == "radio":
                    #handle dialog questions
                    self._handle_dialog_question(label , element)
                elif element[0].get_attribute("type") == "checkbox":
                    #handle dialog questions
                    self._handle_checkbox_question(label , element)
            elif element.get_attribute("type") == "text":
                # handle text based questions
                self._handle_text_question(label, element)
            else:
                #handle dialog questions
                self._handle_select_question(label , element)
