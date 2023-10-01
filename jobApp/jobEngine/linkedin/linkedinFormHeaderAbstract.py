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
from .linkedinDivsAbstract import DivsDocumentUpload, DivsContactInfo, DivsPrivacyPolicy, DivsAdditionalQuestions, DivsHomeAddress
# Abstract base class for headers


class Header(ABC):
    @abstractmethod
    def detect(self, form: WebElement):
        pass

    @abstractmethod
    def fill(self,form, data:CandidateProfile):
        pass

# Concrete header classes


class ContactInfoHeader(Header):
    header = "Contact info"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self,form, data:CandidateProfile):
        try:
            DivHandler = DivsContactInfo()
            divs = DivHandler.find(form) # return divs 
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_contact_infos(
                    data, dict_Elems)
        except:
            print("no contact infos to fill")

class ResumeHeader(Header):
    header = "Resume"

    def detect(self, form: WebElement):
        try:
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self,form, data:CandidateProfile):
        try:
            DivHandler = DivsDocumentUpload()
            divs = DivHandler.find(form) # return divs 
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_documents(
                    data, dict_Elems)
        except:
            print("no resume to fill")

class HomeAddressHeader(Header):
    header = "Home address"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self,form, data:CandidateProfile):
        try:
            DivHandler = DivsHomeAddress()
            divs = DivHandler.find(form) # return divs 
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_contact_infos(
                    data, dict_Elems)
        except:
            print("no home address to fill")

class AdditionalQuestionsHeader(Header):
    header = "Additional Questions"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self,form, data:CandidateProfile):
        try:
            DivHandler = DivsAdditionalQuestions()
            divs = DivHandler.find(form) # return divs 
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_questions_answers(
                    data, dict_Elems)
        except:
            print("no additional questions to fill")

class PrivacyPolicyHeader:
    header = "Privacy policy"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16.t-bold').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text == self.header:
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self,form, data:CandidateProfile):
        try:
            DivHandler = DivsPrivacyPolicy()
            divs = DivHandler.find(form) # return divs 
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.select_privacy_policy(
                    dict_Elems)
        except:
            print("no privacy policy to fill")


class UnkownHeader(Header):
    def detect(self, form: WebElement):
        # Logic to detect the Additional Info header's web element
        pass

    def fill(self,form, data:CandidateProfile):
        # Logic to fill in Additional Info data:CandidateProfile
        pass


# Factory for creating headers
class HeaderFactory:
    def create_header(self, form: WebElement):
        headers = [ContactInfoHeader(), ResumeHeader(),HomeAddressHeader(),
                   AdditionalQuestionsHeader(), PrivacyPolicyHeader()]
        for header in headers:
            if header.detect(form):
                return header
        return UnkownHeader()
        raise ValueError("No header detected")
