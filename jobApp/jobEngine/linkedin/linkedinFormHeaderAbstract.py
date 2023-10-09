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
from concurrent.futures import ThreadPoolExecutor


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
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
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
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
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
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
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



class WorkExperienceHeader(Header):
    header = "Work experience"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False
    # should be filled directly on platform by user
    def fill(self,form, data:CandidateProfile):
        pass

class EducationHeader(Header):
    header = "Education"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False
    # should be filled directly on platform by user
    def fill(self,form, data:CandidateProfile):
        pass

class ScreeningQuestionsHeader(Header):
    header = "Screening questions"
    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False
    # should be filled directly on platform by user
    def fill(self,form, data:CandidateProfile):
        pass

class AdditionalQuestionsHeader(Header):
    headers = ["additional questions", "personal info", "additional"]
    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            translated = googleTranslator.translate(header, dest='en').text.lower()
            if translated in self.headers:
                print("page header translated: ", translated )
                return True
        except:
            print(f"translated {translated} header not in headers")
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
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
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

class ReviewApplicationHeader:
    header = "Review your application"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-18').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ", googleTranslator.translate(header, dest='en').text )
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self,form, data:CandidateProfile):
        print("skipping header submit page")
        pass

class UnkownHeader(Header):
    header = "unkown"
    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            print("new header detected: ", header)
            googleTranslator = Translator()

        except:
            print("no header found")
    def fill(self,form, data:CandidateProfile):
        # Logic to fill in Additional Info data:CandidateProfile
        print("filling unkown header")


class HeaderFactory:
    def create_header(self, form: WebElement):
        headers = [ContactInfoHeader(), ResumeHeader(), HomeAddressHeader(),
                   EducationHeader(), WorkExperienceHeader(), ScreeningQuestionsHeader(),
                   AdditionalQuestionsHeader(), PrivacyPolicyHeader(), ReviewApplicationHeader()]

        def create_header_task(header):
            if header.detect(form):
                return header
            return None

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(create_header_task, headers))

        for result in results:
            if result is not None:
                return result

        return UnkownHeader()






