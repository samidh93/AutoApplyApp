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


class Divs(ABC):
    @abstractmethod
    def find(self, form: WebElement):
        pass

class DivsContactInfo(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(
                By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
            print("found divs with selection grouping")
            if divs != None:
                return divs
        except NoSuchElementException:
            print("No div selection grouping elements found")

    def send_user_contact_infos(self, user: CandidateProfile, divs: [WebElement]):

        def process_contact_info(user: CandidateProfile, div: WebElement):
            try:
                google_translator = Translator()
                text = div.text.split('\n', 1)[0] or div.text
                translation = google_translator.translate(
                    text, dest='en').text.lower()
                if translation == 'first name':
                    LinkedinUtils.send_value(div, user.firstname)
                    print(f"firstname to send: {user.firstname}")
                elif translation == 'last name':
                    LinkedinUtils.send_value(div, user.lastname)
                    print(f"lastname to send: {user.lastname}")
                elif translation == 'phone country code' or translation == 'country code':
                    print("selecting user phone country code: ", user.phone_code)
                    LinkedinUtils.select_option(div, user.phone_code)
                elif translation == 'mobile phone number':
                    LinkedinUtils.send_value(div, user.phone_number)
                    print(f"mobile to send: {user.phone_number}")
                elif translation.split('\n', 1)[0] == 'email address':
                    LinkedinUtils.select_option(div, user.email)
                elif translation == 'city':
                    LinkedinUtils.send_value(div, user.address)
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
                print(f"Error: {e}")

        for div in divs:
            process_contact_info(user, div)

# Concrete Divs classes


class DivsHomeAddress(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(
                By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
            print("found divs with selection grouping")
            if divs != None:
                return divs
        except NoSuchElementException:
            print("No div selection grouping elements found")

    def send_user_contact_infos(self, user: CandidateProfile, divs: [WebElement]):
        for div in divs:
            try:
                google_translator = Translator()
                text = div.text.split('\n', 1)[0] or div.text
                translation = google_translator.translate(text, dest='en').text.lower()
                if translation == 'city':
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
            div_elements = form.find_elements(
                By.XPATH, "//div[contains(@class, 'js-jobs-document-upload__container') and contains(@class, 'display-flex') and contains(@class, 'flex-wrap')]")
            if div_elements != None:
                return div_elements

        except NoSuchElementException:
            print("No upload elements found")
            return False

    def send_user_documents(self, user: CandidateProfile, divs: dict[WebElement]):
        for div in divs:
            try:
                google_translator = Translator()
                text = div.text.split('\n', 1)[0] or div.text
                translation = google_translator.translate(
                    text, dest='en').text.lower()
                if translation == 'Upload resume'.lower():
                    LinkedinUtils.send_value(div, user.resume)
                elif translation == "Upload cover letter".lower():
                    pass
            except:
                raise ValueError("Unsupported label: {}".format(div.text))


################## Most Unpredictable Part #################
class DivsAdditionalQuestions(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(
                By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
            print("found divs with selection grouping")
            if divs != None:
                return divs
        except NoSuchElementException:
            print("No div selection grouping elements found")

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
                print(f"Error processing question: {str(e)}")

                # Submit tasks to the ThreadPoolExecutor
        for div in divs:
            process_elements(div, user)


class DivsPrivacyPolicy(Divs):
    def find(self, form: WebElement):
        try:
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = form.find_elements(
                By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
            print("found divs privacy policy")
            if divs != None:
                return divs
        except NoSuchElementException:
            print("No div selection grouping elements found")

    def select_privacy_policy(self, divs: [WebElement]):
        googleTranslator = Translator()
        for div in divs:
            try:
                if 'PRIVACY POLICY'.lower() in googleTranslator.translate(div.text, dest='en').text.lower():
                    # click accept the privacy policy
                    print("clicking privacy policy")
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
            divs = form.find_elements(
                By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
            print("found divs privacy policy")
            if divs != None:
                return divs
        except NoSuchElementException:
            print("No div selection grouping elements found")

    def select_gender(self, divs: [WebElement], user: CandidateProfile):
        googleTranslator = Translator()
        for div in divs:
            try:
                if 'gender'.lower() in googleTranslator.translate(div.text, dest='en').text.lower():
                    # click accept the privacy policy
                    print("selecting gender")
                    LinkedinQuestions.process_select_question(
                        div, user)
                    return
                else:
                    raise ValueError("Unsupported label: {}".format(div.text))
            except:
                continue
