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
from .linkedinElementsAbstract import LabelElement, InputElement, FieldsetElement, SpanElement, SelectElement, CheckboxOptionsElements
from .linkedinFunctions import LinkedinUtils, LinkedinQuestions
# Abstract base class for Divss
from concurrent.futures import ThreadPoolExecutor
import threading
import logging
import asyncio
logger = logging.getLogger(__name__)

class Divs(ABC):
    @abstractmethod
    def find(self, form: WebElement):
        pass

class DivsContactInfo(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            #divs = form.find_elements(By.CSS_SELECTOR, 'div[data-test-text-entity-list-form-component]')
            divs = form.find_elements(By.CSS_SELECTOR, ".fb-dash-form-element")
            logger.info("found divs with selection grouping")
            if divs != None:
                return divs
        except NoSuchElementException:
            logger.info("No div selection grouping elements found")

    def send_user_contact_infos(self, user: CandidateProfile, divs: [WebElement]):

        def process_contact_info(user: CandidateProfile, div: WebElement):
            try:
                google_translator = Translator()
                text = div.text.split('\n', 1)[0] or div.text
                translation = asyncio.run(google_translator.translate(
                    text, src='de', dest='en')).text.lower()
                if translation in ['first name', 'firstname', 'given name']:
                    LinkedinUtils.send_value(div, user.firstname)
                    logger.info(f"firstname to send: {user.firstname}")
                elif translation in ['last name', 'lastname', 'surname', 'family name'] :
                    LinkedinUtils.send_value(div, user.lastname)
                    logger.info(f"lastname to send: {user.lastname}")
                elif translation in ['phone country code', 'country code', 'phone code']:
                    #logger.info("selecting user phone country code: ", user.phone_code)
                    LinkedinUtils.select_option(div, user.phone_code)
                elif translation in ['phone number', 'phone', 'mobile number', 'mobile phone number']:
                    LinkedinUtils.send_value(div, user.phone_number)
                    logger.info(f"mobile to send: {user.phone_number}")
                elif translation in ['email address', 'e-mail address', 'email', 'e-mail']:
                    LinkedinUtils.select_option(div, user.email)
                elif any(word in translation for word in ['city', 'location']):
                    LinkedinUtils.send_value(div, user.address.city)
                    time.sleep(2)  # wait for the suggestion to appear
                    suggestions = div.find_elements(By.CSS_SELECTOR, "div.basic-typeahead__selectable")
                    # Select the first option that contains "Berlin"
                    for option in suggestions:
                        if "Berlin" in option.text:
                            option.click()
                            break  # Stop after selecting the first matching option 
                elif translation == 'upload resume':
                    LinkedinUtils.send_value(div, user.resume)
                elif translation == "summary":
                    LinkedinUtils.send_value(
                        div, user.generate_summary_for_job())
                elif translation == "headline":
                    # LinkedinUtils.send_value(element, user.summary)
                    pass
                else:
                    raise ValueError("Unsupported label: {}".format(div.text))
            except Exception as e:
                logger.error(f"Error: {e}")

        for div in divs:
            process_contact_info(user, div)

# Concrete Divs classes


class DivsHomeAddress(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(By.CSS_SELECTOR, 'div[data-test-text-entity-list-form-component]')
            logger.info("found divs with selection grouping")
            if divs != None:
                return divs
        except NoSuchElementException:
            logger.info("No div selection grouping elements found")

    def send_user_contact_infos(self, user: CandidateProfile, divs: [WebElement]):
        for div in divs:
            try:
                google_translator = Translator()
                text = div.text.split('\n', 1)[0] or div.text
                translation = asyncio.run(google_translator.translate(text, dest='en')).text.lower()
                if any(word in translation for word in ['city', 'location']):
                    LinkedinUtils.send_value(div, user.address.city)
                    time.sleep(1)  # wait for the suggestion to appear
                    if not LinkedinUtils.choose_option_listbox(div, user.address.city):
                        # just clean and pass
                        div.find_element(By.TAG_NAME, "input").clear()
                elif "street address" in translation:
                    LinkedinUtils.send_value(div, user.address.street)
                elif "postal code" in translation or "zip" in translation:
                    LinkedinUtils.send_value(div, user.address.plz)
                else:
                    raise ValueError("Unsupported label: {}".format(div.text))
            except:
                continue

# Concrete Divs classes


class DivsDocumentUpload(Divs):
    def find(self, form: WebElement):
        try:
            div_elements = form.find_elements(By.CSS_SELECTOR, "div.js-jobs-document-upload__container")
            if div_elements != None:
                return div_elements

        except NoSuchElementException:
            logger.info("No upload elements found")
            return False

    def send_user_documents(self, user: CandidateProfile, divs: dict[WebElement]):
        keywords= ["resume", "cv", "curriculum vitae"]
        for div in divs:
            try:
                google_translator = Translator()
                text = div.text.split('\n', 1)[0] or div.text
                translation = asyncio.run(google_translator.translate(
                    text, dest='en')).text.lower()
                if any(word in translation for word in keywords):
                    LinkedinUtils.send_value(div, user.resume)
                    # wait for 5 seconds until resume upload is complete
                    time.sleep(5)
                elif 'cover letter'.lower() in translation:
                    LinkedinUtils.send_value(div, user.cover_letter)
            except:
                raise ValueError("Unsupported label: {}".format(div.text))


################## Most Unpredictable Part #################
class DivsAdditionalQuestions(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div fb-dash-form-element
            divs = form.find_elements(By.CSS_SELECTOR, 'div.fb-dash-form-element')
            logger.info("found divs with selection grouping")
            if divs != None:
                return divs
        except NoSuchElementException:
            logger.info("No div selection grouping elements found")

    def send_user_questions_answers(self, user: CandidateProfile, divs: [WebElement]):
 
        def process_elements(div:WebElement, user):
            try:
                if LinkedinUtils.isRadioElement(div):
                    # handle radio elems
                    LinkedinQuestions.process_radio_question(
                         div, user)
                elif LinkedinUtils.isCheckboxElement(div):
                    # handle checkbox questions
                    LinkedinQuestions.process_checkbox_question(
                         div, user)
                elif LinkedinUtils.isTextElment(div):
                    # handle text based questions
                    LinkedinQuestions.process_text_question(div, user)
                elif LinkedinUtils.isTextAreaElment(div):
                    LinkedinQuestions.process_text_question(div, user)
                elif LinkedinUtils.isSelectElement(div):
                    # handle select questions
                    LinkedinQuestions.process_select_question(div, user)
            except Exception as e:
                logger.error(f"Error processing question: {str(e)}")

                # Submit tasks to the ThreadPoolExecutor
        for div in divs:
            process_elements(div, user)

    
    def collect_questions(divs: WebElement)->list:
        questions = []
        try:
            for div in divs:
                source_qs = div.text.split('\n', 1)[0] or div.text
                logger.info("Processing select question: %s", source_qs)
                questions.append(source_qs)
        except Exception as e:
            pass
        

class DivsPrivacyPolicy(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(By.CSS_SELECTOR, 'fieldset[data-test-checkbox-form-component]')
            logger.info("found divs privacy policy")
            if divs != None:
                return divs
        except NoSuchElementException:
            logger.info("No div selection grouping elements found")

    def select_privacy_policy(self, divs: [WebElement]):
        googleTranslator = Translator()
        for div in divs:
            try:
                if 'PRIVACY POLICY'.lower() in asyncio.run(googleTranslator.translate(div.text, dest='en')).text.lower():
                    # click accept the privacy policy
                    logger.info("clicking privacy policy")
                    LinkedinQuestions.process_checkbox_question(
                        div, None)
                    return
                else:
                    raise ValueError("Unsupported label: {}".format(div.text))
            except:
                continue


class DivsVoluntarySelfIdentification(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(By.CSS_SELECTOR, 'div[data-test-text-entity-list-form-component]')
            logger.info("found divs privacy policy")
            if divs != None:
                return divs
        except NoSuchElementException:
            logger.info("No div selection grouping elements found")

    def select_gender(self, divs: [WebElement], user: CandidateProfile):
        googleTranslator = Translator()
        for div in divs:
            try:
                if 'gender'.lower() in asyncio.run(googleTranslator.translate(div.text, dest='en')).text.lower():
                    # click accept the privacy policy
                    logger.info("selecting gender")
                    LinkedinQuestions.process_select_question(
                        div, user)
                    return
                else:
                    raise ValueError("Unsupported label: {}".format(div.text))
            except:
                continue
