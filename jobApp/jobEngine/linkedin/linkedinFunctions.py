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
from .linkedinElementsAbstract import LabelElement, InputElement, SpanElement
from datetime import date
import logging
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
                select.select_by_visible_text(select.options[1].accessible_name)     
            if isinstance(select.options, Iterable):
                for option in select.options:
                    translated = googleTranslator.translate(option.accessible_name,src='de', dest='en').text.lower()
                    if user_value.lower() in translated: # if user value is in any of the option
                        select.select_by_visible_text(option.accessible_name)
                        logger.info("user option selected: %s", select.first_selected_option.accessible_name)
                        return 
                # if user value (yes or no or any ) is not part of the option, select first option
                logger.info("user data not found, selecting default first option: %s", select.options[1].accessible_name)
                select.select_by_visible_text(select.options[1].accessible_name)
        except Exception as e:
            logger.error(f"select option error: {e}")

class LinkedinQuestions:
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_text_question( div: WebElement, user:CandidateProfile ):
        googleTranslator = Translator()
        qs_type= "text question"
        try:
            label_translated:str = googleTranslator.translate(div.text, dest='en').text # translate qs to en
            logger.info("processing translated text question: %s", label_translated)
            start_date_keywords = ["start date", "earliest", "notice period", "when", "available from"]
            platform_keywords = ["aware of us", "find out about us"]
            experience_keywords =["how many", "years", "experience", "how long"]
            if "salary" in label_translated.lower():
                LinkedinUtils.send_value(div, user.desired_salary)
            elif any(keyword in label_translated.lower() for keyword in experience_keywords):
                LinkedinUtils.send_value(div, user.years_experience)
            elif any(keyword in label_translated.lower() for keyword in start_date_keywords):
                LinkedinUtils.send_value(div, user.earliest_start_date )
            elif any(keyword in label_translated.lower() for keyword in platform_keywords):
                LinkedinUtils.send_value(div, user.current_job.platform )
            elif "city" in label_translated.lower():
                LinkedinUtils.send_value(div, user.address.city)
            elif "country" in label_translated.lower():
                LinkedinUtils.send_value(div, user.country_name)
            elif "name" in label_translated.lower():
                LinkedinUtils.send_value(div, user.firstname)
            elif "willing" or "move" in label_translated.lower():
                LinkedinUtils.send_value(div, "yes" )
        except:
            logger.info(f"unable to process {qs_type}") 

    @staticmethod
    def process_radio_question( div: WebElement, user:CandidateProfile ):
        googleTranslator = Translator()
        qs_type= "radio question"
        try:
            source_qs = div.text.split('\n', 1)[0] or div.text
            logger.info("processing radio question: %s", source_qs)
            elements = div.find_elements(By.TAG_NAME, "label")
            for element in elements:
                logger.info("radio option: %s", element.text)
                source_lang = googleTranslator.translate(source_qs, dest='en').src
                translated = googleTranslator.translate(element.text.lower().strip(), src=source_lang,dest='en').text.lower() 
                if translated == "yes":
                    if not element.is_selected():
                        element.click()
                        logger.info(f"element {translated} clicked successfully.")
                        return
        except:
            logger.info(f"unable to process {qs_type}") 
    @staticmethod
    def process_select_question( div: WebElement, user:CandidateProfile ):
        qs_type= "select question"
        googleTranslator = Translator()
        try:
            logger.info("processing select question: %s", div.text.split('\n', 1)[0])
            label_translated:str = googleTranslator.translate(div.text.split('\n', 1)[0], dest='en').text.lower() # translate qs to en
            # handle languages questions : basic , good etc.. 
            if "english" in label_translated.lower():
                    LinkedinUtils.select_option(div, user.skills.languages.get_level("english")) 
            elif "german" in label_translated.lower():
                    LinkedinUtils.select_option(div, user.skills.languages.get_level("german")) 
            elif "experience" in label_translated.lower():
                LinkedinUtils.select_option(div, user.years_experience)
            elif "visa" in label_translated.lower():
                LinkedinUtils.select_option(div, user.visa_required)
            elif "how did you" in label_translated.lower():
                LinkedinUtils.select_option(div, user.current_job.platform)
            elif "gender" in label_translated.lower():
                LinkedinUtils.select_option(div, user.gender)
            # handle questions that can be answered by yes or no
            elif "do you" in label_translated.lower() or "have you" in label_translated.lower() or "are your" in label_translated.lower():
                LinkedinUtils.select_option(div, "yes")
            else:
                LinkedinUtils.select_option(div, "first")

        except:
            logger.info(f"unable to process {qs_type}") 


    @staticmethod
    def process_checkbox_question( div: WebElement, user:CandidateProfile):
        qs_type= "checkbox question"
        googleTranslator = Translator()

        try:
            legend = div.find_element(By.TAG_NAME, "legend")
            logger.info("checkbox question: %s", legend.text.strip() )
            # if only one checkbox to click, just click it if is not already clicked
            checkboxElems:[WebElement] = div.find_elements(By.TAG_NAME, "label")
            if len(checkboxElems) == 1:
                if not checkboxElems[0].is_selected():
                    checkboxElems[0].click()
                    logger.info(f"element clicked successfully.")
                    return 
            for element in checkboxElems:
                #for opt_label in label_options:
                    logger.info("checkbox option: %s", element.text)
                    translated = googleTranslator.translate(element.text.lower(), dest='en').text.lower()
                    if googleTranslator.translate("I Agree Terms & Conditions", dest='en').text.lower() in translated:
                        if not element.is_selected():
                            element.click()
                            logger.info(f"element {translated} clicked successfully.")
                            return
                    elif googleTranslator.translate("Are you willing", dest='en').text.lower() in translated:
                        if not element.is_selected():
                            element.click()
                            logger.info(f"element {translated} clicked successfully.")
                            return          
        except Exception as e:
            logger.error(f"unable to process {qs_type}, error {e}") 
    