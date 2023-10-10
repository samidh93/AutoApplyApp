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
from .linkedinDivsAbstract import DivsDocumentUpload, DivsContactInfo, DivsPrivacyPolicy, DivsAdditionalQuestions, DivsHomeAddress, DivsVoluntarySelfIdentification
from concurrent.futures import ThreadPoolExecutor, Future
import concurrent.futures
import threading

# Abstract base class for headers


class Header(ABC):
    @abstractmethod
    def detect(self, form: WebElement):
        pass

    @abstractmethod
    def fill(self, form, data: CandidateProfile):
        pass

# Concrete header classes


class ContactInfoHeader(Header):
    header = "Contact info"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            translated = googleTranslator.translate(header, dest='en').text.lower()
            print("page header translated: ", translated)
            if translated == self.header.lower():
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsContactInfo()
            divs = DivHandler.find(form)  # return divs
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
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsDocumentUpload()
            divs = DivHandler.find(form)  # return divs
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
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsHomeAddress()
            divs = DivHandler.find(form)  # return divs
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
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False
    # should be filled directly on platform by user

    def fill(self, form, data: CandidateProfile):
        pass


class EducationHeader(Header):
    header = "Education"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False
    # should be filled directly on platform by user

    def fill(self, form, data: CandidateProfile):
        pass


class ScreeningQuestionsHeader(Header):
    header = "Screening questions"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False
    # should be filled directly on platform by user

    def fill(self, form, data: CandidateProfile):
        pass


class AdditionalQuestionsHeader(Header):
    headers = ["additional questions", "personal info", "additional"]

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            translated = googleTranslator.translate(
                header, dest='en').text.lower()
            if translated in self.headers:
                print("page header translated: ", translated)
                return True
        except:
            print(f"translated {translated} header not in headers")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsAdditionalQuestions()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_questions_answers(
                    data, dict_Elems)
        except:
            print("no additional questions to fill")


class PrivacyPolicyHeader(Header):
    header = "Privacy policy"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsPrivacyPolicy()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.select_privacy_policy(
                    dict_Elems)
        except:
            print("no privacy policy to fill")


class ReviewApplicationHeader(Header):
    header = "Review your application"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-18').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        print("skipping header submit page")
        pass


class VoluntarySelfIdentification(Header):
    header = "Voluntary self identification"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.TAG_NAME, 'h3').text
            googleTranslator = Translator()
            if googleTranslator.translate(header, dest='en').text.lower() == self.header.lower():
                print("page header translated: ",
                      googleTranslator.translate(header, dest='en').text)
                return True
        except:
            print(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsVoluntarySelfIdentification()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.select_gender(
                    dict_Elems, data)
        except:
            print("no privacy policy to fill")


class UnknownHeader(Header):
    header = "unkown"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            print("new header detected: ", header)
            googleTranslator = Translator()

        except:
            print("no header found")

    def fill(self, form, data: CandidateProfile):
        # Logic to fill in Additional Info data:CandidateProfile
        print("filling unkown header")
        try:
            DivHandler = DivsAdditionalQuestions()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # create the key,value pair for each element on the form
                dict_Elems = DivHandler.createDictFromDivs(divs)
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_questions_answers(
                    user=data, elements_dict=dict_Elems)
        except:
            print("no data to fill")


class HeaderFactory:

    def create_header(self, form: WebElement):
        headers = [ContactInfoHeader(), ResumeHeader(), HomeAddressHeader(),
                   EducationHeader(), WorkExperienceHeader(), ScreeningQuestionsHeader(),
                   AdditionalQuestionsHeader(), PrivacyPolicyHeader(), ReviewApplicationHeader(),
                   VoluntarySelfIdentification()]

        # Create an event to signal when a header is found
        header_found_event = threading.Event()
        form_lock = threading.Lock()
        def create_header_task(header: Header):
            try:
                with form_lock:
                    if header.detect(form):
                        header_found_event.set()  # Signal that a header is found
                        return header
            except Exception as e:
                print(f"Error in create_header_task: {e}")
            return None

        # Create a Future object for each header
        futures = []
        with ThreadPoolExecutor(max_workers=len(headers)) as executor:
            for header in headers:
                if not header_found_event.is_set():
                    futures.append(executor.submit(create_header_task, header))
                else:
                    break  # Cancel the loop if a header is found

            # Wait for any of the threads to find a header
            concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

            # Cancel all remaining tasks in the pool
            for future in futures:
                if not future.done():
                    future.cancel()

            # Find the header that was detected and return it
            for future in futures:
                if future.done() and future.result():
                    print(future.result().header)
                    return future.result()

        # Return UnknownHeader if no header was found
        return UnknownHeader()