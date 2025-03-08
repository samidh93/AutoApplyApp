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
import logging
logger = logging.getLogger(__name__)
import asyncio

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
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            logger.info("page header translated: %s", translated)
            if translated == self.header.lower():
                return True
        except:
            logger.warning(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsContactInfo()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # fill the form with candidate data:CandidateProfile
                logger.info("skip filling contact info")
                #DivHandler.send_user_contact_infos(
                #    data, divs)
        except:
            logger.warning("no contact infos to fill")


class ResumeHeader(Header):
    headers = ["resume", "cv"]

    def detect(self, form: WebElement):
        try:
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated in self.headers:
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.headers[0]} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsDocumentUpload()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_documents(
                    data, divs)
        except:
            logger.warning("no resume to fill")


class HomeAddressHeader(Header):
    header = "Home address"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated == self.header.lower():
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsHomeAddress()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_contact_infos(
                    data, divs)
        except:
            logger.warning("no home address to fill")


class WorkExperienceHeader(Header):
    header = "Work experience"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated == self.header.lower():
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.header} header found")
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
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated == self.header.lower():
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.header} header found")
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
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated == self.header.lower():
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.header} header found")
            return False
    # should be filled directly on platform by user

    def fill(self, form, data: CandidateProfile):
        pass


class AdditionalQuestionsHeader(Header):
    headers = [
        "additional questions",
        "personal info",
        "additional",
        "questions",
        "further questions",
    ]

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated in self.headers:
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.headers[0]} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsAdditionalQuestions()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_questions_answers(
                    data, divs)
            logger.info("finished filling header additional questions")
        except:
            logger.warning("no additional questions to fill")


class PrivacyPolicyHeader(Header):
    header = "Privacy policy"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated == self.header.lower():
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsPrivacyPolicy()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # fill the form with candidate data:CandidateProfile
                DivHandler.select_privacy_policy(
                    divs)
        except:
            logger.warning("no privacy policy to fill")


class ReviewApplicationHeader(Header):
    header = "Review your application"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-18').text
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated == self.header.lower():
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        logger.info("skipping header submit page")
        pass


class VoluntarySelfIdentification(Header):
    header = "Voluntary self identification"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.TAG_NAME, 'h3').text
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            if translated == self.header.lower():
                logger.info("page header translated: %s", translated)
                return True
        except:
            logger.info(f"no {self.header} header found")
            return False

    def fill(self, form, data: CandidateProfile):
        try:
            DivHandler = DivsVoluntarySelfIdentification()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # fill the form with candidate data:CandidateProfile
                DivHandler.select_gender(
                    divs, data)
        except:
            logger.warning("no privacy policy to fill")


class UnknownHeader(Header):
    header = "unkown"

    def detect(self, form: WebElement):
        try:
            # Find the <h3> element with class "t-16 t-bold".
            header = form.find_element(By.CSS_SELECTOR, 'h3.t-16').text
            logger.info("new header detected: %s", header)
            googleTranslator = Translator()
            # Run the coroutine to get the translation result.
            translation_result = asyncio.run(googleTranslator.translate(header, dest='en'))
            # Now access the 'text' attribute and convert to lowercase.
            translated = translation_result.text.lower()
            logger.info("new header translated: %s", translated)
        except:
            logger.warning("no header found")

    def fill(self, form, data: CandidateProfile):
        # Logic to fill in Additional Info data:CandidateProfile
        logger.info("filling unkown header")
        try:
            DivHandler = DivsAdditionalQuestions()
            divs = DivHandler.find(form)  # return divs
            if len(divs) != 0:
                # fill the form with candidate data:CandidateProfile
                DivHandler.send_user_questions_answers(
                    data, divs)
        except:
            logger.warning("no data to fill")


class HeaderFactory:

    def create_header(self, form: WebElement):
        #ContactInfoHeader(),
        headers = [ ContactInfoHeader(),ResumeHeader(), 
                   HomeAddressHeader(),EducationHeader(), 
                   WorkExperienceHeader(), ScreeningQuestionsHeader(), 
                   AdditionalQuestionsHeader(), PrivacyPolicyHeader(), 
                   ReviewApplicationHeader(),VoluntarySelfIdentification()]

        def create_header_task(header: Header):
            try:
                if header.detect(form):
                    return header
            except Exception as e:
                logger.error(f"Error in create_header_task: {e}")
                return None
        for header in headers:
            head = create_header_task(header)
            if head != None: # found header
                return head
        # Return UnknownHeader if no header was found
        return UnknownHeader()