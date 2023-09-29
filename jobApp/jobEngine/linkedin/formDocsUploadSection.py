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

class FormDocumentHandler():
    def __init__(self) -> None:
        pass

    def _fill_resume(self, form: WebElement):
        self.label_elements_map.clear()
        try:
            divs = self._find_divs_document_upload()
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                self._createDictFromFormDiv(divs)
                # fill the form with candidate data
                self._send_user_documents(self.candidate, self.label_elements_map)
                # click next buttton
                self.label_elements_map.clear()
        except:
            print("no resume to fill")

    def _send_user_documents(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        for label, element in elements_dict.items():
            if label == 'Upload resume':
                self.send_value(element, user.resume)
            elif label == "Upload cover letter": # ignore cover letter: need specification later
                pass
            else:
                raise ValueError("Unsupported label: {}".format(label))

    def _find_divs_document_upload(self) -> list[WebElement]:
        if self.form != None:  # if form is found
            try:
                div_elements = self.form.find_elements(
                    By.XPATH, "//div[contains(@class, 'js-jobs-document-upload__container') and contains(@class, 'display-flex') and contains(@class, 'flex-wrap')]")
                return div_elements
            except NoSuchElementException:
                print("No upload elements found")
