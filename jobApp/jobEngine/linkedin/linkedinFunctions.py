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

class LinkedinUtils:
    def __init__(self) -> None:
        pass
    @staticmethod
    def send_value( element: WebElement, value: str):
        element_type = element.get_attribute("type")
        if element_type == "file":
            print(f"sending file path: {value}")
            element.send_keys(value)
        elif element_type == "text":
            element.clear()
            element.send_keys(value)
        else:
            print("input type not recognized")
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
    def select_option( select_element, user_value):
        select = Select(select_element)
        if isinstance(select.options, Iterable):
            for option in select.options:
                if user_value in option.accessible_name: # if user value is in any of the option
                    select.select_by_visible_text(user_value)
                    print("user option selected: ", select.first_selected_option.accessible_name)
                    return 
            # if user value (yes or no or any ) is not part of the option, select first option
            select.select_by_visible_text(select.options[1])

class LinkedinQuestions:
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_text_question( label:WebElement, element: WebElement, user:CandidateProfile ):
        googleTranslator = Translator()
        qs_type= "text question"
        try:
            print("processing text question: ", label.text)
            label_translated:str = googleTranslator.translate(label.text, dest='en').text # translate qs to en
            if "salary" in label_translated.lower():
                LinkedinUtils.send_value(element, user.desired_salary)
            elif "experience" in label_translated.lower():
                LinkedinUtils.send_value(element, user.years_experience)
        except:
            print(f"unable to process {qs_type}") 
    @staticmethod
    def process_radio_question( label:WebElement, element: WebElement, user:CandidateProfile ):
        googleTranslator = Translator()
        spanObj = SpanElement()
        qs_type= "radio question"
        try:
            spanElem:WebElement = spanObj.find(element)
            print("processing radio question: ", spanElem.text.strip())
            input_options = element.find_elements(By.TAG_NAME, "input")
            for opt in input_options:
                radio_value= opt.get_attribute("value").lower()
                print("radio option: ", radio_value)
                if radio_value == googleTranslator.translate("yes", dest='en').text:
                    opt.click()
        except:
            print(f"unable to process {qs_type}") 
    @staticmethod
    def process_select_question( label:WebElement, element: WebElement, user:CandidateProfile ):
        qs_type= "select question"
        googleTranslator = Translator()
        try:
            print("processing select question: ", label.text)
            label_translated:str = googleTranslator.translate(label.text, dest='en').text # translate qs to en
            # handle questions that can be answered by yes or no
            if "do you" in label_translated.lower() or "have you" in label_translated.lower() or "are your" in label_translated.lower():
                LinkedinUtils.select_option(element, "yes")
            # handle languages questions : basic , good etc.. 
            if "how good" in label_translated.lower(): # this is meanted to expand to each languages "how good" + "english"
                if "english" in label_translated.lower():
                    LinkedinUtils.select_option(element, user.skills.languages.get_level("en")) 
                elif "german" in label_translated.lower():
                    LinkedinUtils.select_option(element, user.skills.languages.get_level("de")) 
            elif "visa" in label_translated.lower():
                LinkedinUtils.select_option(element, user.visa_required)
        except:
            print(f"unable to process {qs_type}") 


    @staticmethod
    def process_checkbox_question( label:WebElement, element: WebElement, user:CandidateProfile):
        qs_type= "checkbox question"
        googleTranslator = Translator()
        spanObj = SpanElement()
        try:
            spanElem:WebElement = spanObj.find(element)
            print("checkbox question: ", spanElem.text.strip() )
            # random value in the middle
            # Find the associated label using its attributes (for or id) or relationship (preceding-sibling, following-sibling, etc.)
            input_options = element.find_elements(By.TAG_NAME, "input")
            label_options = element.find_elements(By.TAG_NAME, "label")
            for opt in input_options:
                for label in label_options:
                    print("radio option: ", label.text)
                    if label.text.lower() == googleTranslator.translate("I Agree Terms & Conditions", dest='en').text.lower():
                        if not opt.is_selected():
                            opt.click()
                            print(f"Label {label.text} clicked successfully.")

        except Exception as e:
            print(f"unable to process {qs_type}") 

