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
    label_elements_map = {}
    lock = threading.Lock()  # Create a lock for synchronization

    @abstractmethod
    def find(self, form: WebElement):
        pass

    def createDictFromDivs(self, divs):
        self.label_elements_map.clear()
        field = FieldsetElement()
        label = LabelElement()

        def process_div(div):
            try:
                print("processing form fields")
                fieldset = field.find(div)
                if fieldset is not None:
                    return field.handle(fieldset)
                else:
                    labelElem = label.find(div)
                    if labelElem is not None:
                        return label.handle(div, labelElem)
            except Exception as e:
                print(f"Error processing div: {e}")
            return {}

        for div in divs:
            result =  process_div(div) 
            if result != {}:
                self.label_elements_map.update(result)

        return self.label_elements_map

# Concrete Divs classes
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

    def send_user_contact_infos(self, user: CandidateProfile, elements_dict: dict[WebElement]):

        def process_contact_info( user:CandidateProfile, label, element):
                try:
                    google_translator = Translator()
                    translation = google_translator.translate(label.text, dest='en').text.lower()
                    if translation == 'first name':
                        LinkedinUtils.send_value(element, user.firstname)
                        print(f"firstname to send: {user.firstname}")
                    elif translation == 'last name':
                        LinkedinUtils.send_value(element, user.lastname)
                        print(f"lastname to send: {user.lastname}")
                    elif translation.split('\n', 1)[0] == 'phone country code' or 'country code':
                        print("selecting user phone country code: ", user.phone_code)
                        LinkedinUtils.select_option(element, user.phone_code)
                    elif translation == 'mobile phone number':
                        LinkedinUtils.send_value(element, user.phone_number)
                        print(f"mobile to send: {user.phone_number}")
                    elif translation.split('\n', 1)[0] == 'email address':
                        LinkedinUtils.select_option(element, user.email)
                    elif translation == 'city':
                        LinkedinUtils.send_value(element, user.address)
                    elif translation == 'upload resume':
                        LinkedinUtils.send_value(element, user.resume)
                    elif translation == "summary":
                        LinkedinUtils.send_value(element, user.generate_summary_for_job())
                    elif translation == "headline":
                        # LinkedinUtils.send_value(element, user.summary)
                        pass
                    else:
                        raise ValueError("Unsupported label: {}".format(label))
                except Exception as e:
                    print(f"Error: {e}")

        for label, element in elements_dict.items():
            process_contact_info( user, label, element)
   

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

    def send_user_documents(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        googleTranslator = Translator()
        for label, element in elements_dict.items():
            if googleTranslator.translate(label.text, dest='en').text == 'Upload resume':
                LinkedinUtils.send_value(element, user.resume)
            elif googleTranslator.translate(label.text, dest='en').text == "Upload cover letter":
                pass
            else:
                raise ValueError("Unsupported label: {}".format(label))

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

    def send_user_contact_infos(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        googleTranslator = Translator()
        for label, element in elements_dict.items():
            try:
                translated:str = googleTranslator.translate(label.text.split('\n', 1)[0], dest='en').text.lower()
                print("translated adress: ", translated)
                if  translated== 'city':
                    LinkedinUtils.send_value(element, user.address.city)
                    time.sleep(1) # wait for the suggestion to appear
                    if not LinkedinUtils.choose_option_listbox(element, user.address.city):
                        # just clean and pass
                        element.clear()
                elif "street address" in translated :
                    LinkedinUtils.send_value(element, user.address.street)
                elif "postal code" in translated or "plz" in translated:
                    LinkedinUtils.send_value(element, user.address.plz)
                else:
                    raise ValueError("Unsupported label: {}".format(label))
            except:
                continue

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

    def send_user_questions_answers(self, user: CandidateProfile, elements_dict: dict[WebElement]):
            # Create a ThreadPoolExecutor with a specified number of threads
            max_threads = len(elements_dict)  # You can adjust the number of threads as needed
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Define a function to process each set of elements
                def process_elements(label, elements, user):
                    try:
                        if isinstance(elements, list):
                            elem_type: WebElement = elements[0].find_element(By.TAG_NAME, "input").get_attribute("type")
                            if elem_type == "radio":
                                # handle dialog questions
                                LinkedinQuestions.process_radio_question(label, elements, user)
                            elif elem_type == "checkbox":
                                # handle checkbox questions
                                LinkedinQuestions.process_checkbox_question(label, elements, user)
                        elif elements.get_attribute("type") == "text" or elements.tag_name == 'textarea':
                            # handle text based questions
                            LinkedinQuestions.process_text_question(label, elements, user)
                        else:
                            # handle select questions
                            LinkedinQuestions.process_select_question(label, elements, user)
                    except Exception as e:
                        print(f"Error processing question: {str(e)}")

                # Submit tasks to the ThreadPoolExecutor
                for label, elements in elements_dict.items():
                    executor.submit(process_elements, label, elements, user)


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

    def select_privacy_policy(self, elements_dict: dict[WebElement]):
        googleTranslator = Translator()
        for label, elements in elements_dict.items():
            try:
                if 'PRIVACY POLICY'.lower() in googleTranslator.translate(label.text, dest='en').text.lower() :
                    # click accept the privacy policy
                    print("clicking privacy policy")
                    LinkedinQuestions.process_checkbox_question(label,elements, None)
                    return 
                else:
                    raise ValueError("Unsupported label: {}".format(label))
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

    def select_gender(self, elements_dict: dict[WebElement] , user:CandidateProfile):
        googleTranslator = Translator()
        for label, elements in elements_dict.items():
            try:
                if 'gender'.lower() in googleTranslator.translate(label.text, dest='en').text.lower() :
                    # click accept the privacy policy
                    print("selecting gender")
                    LinkedinQuestions.process_select_question(label,elements,user)
                    return 
                else:
                    raise ValueError("Unsupported label: {}".format(label))
            except:
                continue


