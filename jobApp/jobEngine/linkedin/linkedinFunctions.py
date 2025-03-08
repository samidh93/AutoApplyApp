from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time
from ..user.candidateProfile import CandidateProfile
from collections.abc import Iterable
from googletrans import Translator
from .linkedinElementsAbstract import LabelElement, InputElement, SpanElement
from datetime import date
import logging
import asyncio
from ..ai.formFiller import FormFiller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
logger = logging.getLogger(__name__)

class LinkedinUtils:
    def __init__(self) -> None:
        pass
    @staticmethod
    def isTextElment(div:WebElement)->bool:
        try:
            if div.find_element(By.TAG_NAME , "input").get_attribute("type") == "text":
                return True
        except:
                return False
    @staticmethod
    def isTextAreaElment(div:WebElement)->bool:
        try:
            if div.find_element(By.TAG_NAME, "textarea" ).tag_name == 'textarea':
                return True
        except:
                return False
    @staticmethod
    def isRadioElement(div:WebElement)->bool:
        try:
            if div.find_elements(By.TAG_NAME,"input")[0].get_attribute("type") == "radio":
                return True
        except:
            return False
        
    @staticmethod
    def isCheckboxElement(div:WebElement)->bool:
        try:
            if div.find_elements(By.TAG_NAME,"input")[0].get_attribute("type") == "checkbox":
                return True
        except:
            return False
    @staticmethod
    def isSelectElement(div:WebElement)->bool:
        try:
            if div.find_element(By.TAG_NAME,"select").tag_name == "select":
                return True
        except:
            return False
    @staticmethod
    def send_value( element: WebElement, value: str):
        try:
            inputElem =element.find_element(By.TAG_NAME, "input")
            element_type = inputElem.get_attribute("type")
            if element_type == "file":
                logger.info(f"sending file path: {value}")
                inputElem.send_keys(value)
            elif element_type == "text":
                logger.info(f"sending text: {value}")
                inputElem.clear()
                inputElem.send_keys(value)
        except:
            logger.info("not an input tag, try textarea")
            textarea =element.find_element(By.TAG_NAME, "textarea")
            textarea.clear()
            textarea.send_keys(value)   

    @staticmethod
    def choose_option_listbox(element: WebElement, value:str):
        try:
            options = element.find_elements(By.XPATH, '//div[@role="option"]')
            for opt in options:
                logger.info(f"user value: {value.lower()}, option value: {opt.text.lower()}")
                if value.lower() in opt.text.lower():
                    opt.click()
                    return True
        except:
            logger.info("no auto fill option found ")
            return False
            
        
    @staticmethod
    def click_option( element: WebElement, value: str):
        element_type = element.get_attribute("type")
        if element_type == "radio":
            for elem in element:
                if elem == value:
                    elem.click()
        elif element_type == "checkbox":
            for elem in element:
                if elem == value:
                    elem.click()
    @staticmethod
    def select_option( div:WebElement, user_value:str):
        googleTranslator = Translator()
        try:
            select_element = div.find_element(By.TAG_NAME, "select")
            select = Select(select_element)
            if user_value == "first" or None:
                logger.info("no user data to the qs, selecting default first option: %s", select.options[1].accessible_name)
                select.select_by_visible_text(select.options[1].text)     
            if isinstance(select.options, Iterable):
                for option in select.options:
                    try:
                        translated = asyncio.run(googleTranslator.translate(option.text.strip(),src='auto', dest='en')).text.lower()
                    except:
                        logger.info("unable to translate option text: %s", option.text)
                        #continue
                    if user_value.lower() in translated: # if user value is in any of the option
                        select.select_by_visible_text(option.text)
                        logger.info("user option selected: %s", select.first_selected_option.text)
                        return 
                # if user value (yes or no or any ) is not part of the option, select first option
                first_option = select.options[1].text
                logger.info("user data not found, selecting default first option: %s", first_option)
                select.select_by_visible_text(first_option)
        except Exception as e:
            logger.error(f"select option error: {e}")

class LinkedinQuestions:
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_text_question(div: WebElement, user: CandidateProfile):
        qs_type = "text question"
        try:
            source_qs = div.text.split('\n', 1)[0] or div.text
            logger.info("processing text question: %s", source_qs)
            
            # Send question to AI
            answer = user.formfiller.answer_question(source_qs)
            
            # If answer is not empty, send the value to the input field
            if answer and len(answer) > 0:
                LinkedinUtils.send_value(div, answer[0])
                logger.info(f"Text field filled with: {answer[0]}")
                return
            
            # Fallback to default value if AI didn't provide an answer
            LinkedinUtils.send_value(div, "Yes")
            logger.info("Used default value: Yes")
            
        except Exception as e:
            logger.warning(f"Unable to process {qs_type}: {e}")

    @staticmethod
    def process_radio_question(div: WebElement, user: CandidateProfile):
        googleTranslator = Translator()
        qs_type = "radio question"
        try:
            source_qs = div.text.split('\n', 1)[0] or div.text
            logger.info("processing radio question: %s", source_qs)
            elements = div.find_elements(By.TAG_NAME, "label")
            options = ", ".join([element.text for element in elements])
            # send question to ai
            question_with_options = source_qs + " options: " + options
            answer = user.formfiller.answer_question(question_with_options)
            # if answer is not empty, click the option
            if answer:
                for element in elements:
                    if answer[0].lower() in element.text.lower():
                        if not element.is_selected():
                            element.click()
                            logger.info(f"element {answer[0]} clicked successfully.")
                            return
        except Exception as e:
            logger.warning(f"Unable to process {qs_type}: {e}")
            try:
                elements = div.find_elements(By.TAG_NAME, "label")
                elements[0].click()
                logger.info(f"element {elements[0].text} clicked instead.")
            except Exception as e2:
                logger.error(f"Failed to click default option: {e2}")

    @staticmethod
    def process_select_question(div: WebElement, user: CandidateProfile):
        qs_type = "select question"
        
        try:
            source_qs = div.text.split('\n', 1)[0] or div.text
            logger.info("Processing select question: %s", source_qs)
            driver = div._parent
            wait = WebDriverWait(driver, 10)  # Adjust timeout if needed
            select = Select(div.find_element(By.TAG_NAME, "select"))
            options = [option.text for option in select.options if option.text.strip()]
            options_text = ", ".join(options)
            question_with_options = source_qs + " options: " + options_text
            answer = user.formfiller.answer_question(question_with_options)
            logger.info(f"AI answer: {answer}")
            if answer and len(answer) > 0:
                for option in select.options:
                    if answer[0].lower() in option.text.lower():
                        option_text = option.text.strip()
                        option.click()
                        logger.info(f"Selected default option: {option_text}")
                        break
        except Exception as e:
            logger.warning(f"Unable to process {qs_type}: {e}")


    @staticmethod
    def process_checkbox_question(div: WebElement, user: CandidateProfile):
        qs_type = "checkbox question"
        try:
            # Try to get the question text from legend or div text
            try:
                legend = div.find_element(By.TAG_NAME, "legend")
                source_qs = legend.text.strip()
            except:
                source_qs = div.text.split('\n', 1)[0] or div.text
            
            logger.info("processing checkbox question: %s", source_qs)
            
            # Get all checkbox options
            checkboxElems = div.find_elements(By.TAG_NAME, "label")
            options = [elem.text for elem in checkboxElems]
            options_text = ", ".join(options)
            
            # Special case for single checkbox
            if len(checkboxElems) == 1:
                if not checkboxElems[0].is_selected():
                    checkboxElems[0].click()
                    logger.info(f"Single checkbox clicked: {checkboxElems[0].text}")
                return
            
            # For multiple checkboxes, ask AI which ones to select
            question_with_options = source_qs + " options: " + options_text
            answer = user.formfiller.answer_question(question_with_options)
            
            if answer and len(answer) > 0:
                selected_options = [opt.strip() for opt in answer[0].split(',')]
                selected_count = 0
                
                for element in checkboxElems:
                    for selected_option in selected_options:
                        if selected_option.lower() in element.text.lower():
                            if not element.is_selected():
                                element.click()
                                selected_count += 1
                                logger.info(f"Checkbox selected: {element.text}")
                
                if selected_count > 0:
                    return
            
            # If nothing was selected, select the first option as fallback
            if len(checkboxElems) > 0 and not any(elem.is_selected() for elem in checkboxElems):
                checkboxElems[0].click()
                logger.info(f"Selected default checkbox: {checkboxElems[0].text}")
                
        except Exception as e:
            logger.warning(f"Unable to process {qs_type}: {e}")


      