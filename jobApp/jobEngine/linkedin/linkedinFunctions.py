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

class LinkedinUtils:
    def __init__(self) -> None:
        pass
    @staticmethod
    def send_value( element: WebElement, value: str):
        try:
            element_type = element.get_attribute("type")
            if element_type == "file":
                print(f"sending file path: {value}")
                element.send_keys(value)
            elif element_type == "text":
                element.clear()
                element.send_keys(value)
            else: #textarea
                element.clear()
                element.send_keys(value)       
        except:
            print("input type not recognized")

    @staticmethod
    def choose_option_listbox(element: WebElement, value:str):
        try:
            options = element.find_elements(By.XPATH, '//div[@role="option"]')
            for opt in options:
                print(f"user value: {value.lower()}, option value: {opt.text.lower()}")
                if value.lower() in opt.text.lower():
                    opt.click()
                    return True
        except:
            print("no auto fill option found ")
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
    def select_option( select_element, user_value:str):
        select = Select(select_element)
        if user_value == "first":
            print("no user data, selecting default first option: ", select.options[1].accessible_name)
            select.select_by_visible_text(select.options[1].accessible_name)     
        if isinstance(select.options, Iterable):
            for option in select.options:
                if user_value.lower() in option.accessible_name.lower(): # if user value is in any of the option
                    select.select_by_visible_text(option.accessible_name)
                    print("user option selected: ", select.first_selected_option.accessible_name)
                    return 
                # else: send user data and options to chatgpt and let it choose
            # if user value (yes or no or any ) is not part of the option, select first option
            print("user data not found, selecting default first option: ", select.options[1].accessible_name)
            select.select_by_visible_text(select.options[1].accessible_name)

class LinkedinQuestions:
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_text_question( label:WebElement, element: WebElement, user:CandidateProfile ):
        googleTranslator = Translator()
        qs_type= "text question"
        try:
            label_translated:str = googleTranslator.translate(label.text, dest='en').text # translate qs to en
            print("processing translated text question: ", label_translated)
            start_date_keywords = ["start date", "earliest", "notice period", "when"]
            platform_keywords = ["aware of us", "find out about us"]
            if "salary" in label_translated.lower():
                LinkedinUtils.send_value(element, user.desired_salary)
            elif "experience" in label_translated.lower():
                LinkedinUtils.send_value(element, user.years_experience)
            elif any(keyword in label_translated.lower() for keyword in start_date_keywords):
                LinkedinUtils.send_value(element, user.earliest_start_date )
            elif any(keyword in label_translated.lower() for keyword in platform_keywords):
                LinkedinUtils.send_value(element, "linkedin" )
            elif "city" in label_translated.lower():
                LinkedinUtils.send_value(element, user.address.city)
            elif "country" in label_translated.lower():
                LinkedinUtils.send_value(element, user.country_name)
            elif "name" in label_translated.lower():
                LinkedinUtils.send_value(element, user.firstname)
            elif "willing" or "move" in label_translated.lower():
                LinkedinUtils.send_value(element, "yes" )
        except:
            print(f"unable to process {qs_type}") 

    @staticmethod
    def process_radio_question( label:WebElement, elements: WebElement, user:CandidateProfile ):
        googleTranslator = Translator()
        qs_type= "radio question"
        try:
            print("processing radio question: ", label.text.strip())
            for element in elements:
                print("radio option: ", element.text)
                if element.text.lower() == googleTranslator.translate("yes", dest='en').text.lower():
                    label = element.find_element(By.TAG_NAME, "label")
                    if not label.is_selected():
                        label.click()
                        print(f"element {element.text} clicked successfully.")
                        return
        except:
            print(f"unable to process {qs_type}") 
    @staticmethod
    def process_select_question( label:WebElement, element: WebElement, user:CandidateProfile ):
        qs_type= "select question"
        googleTranslator = Translator()
        try:
            print("processing select question: ", label.text.split('\n', 1)[0])
            label_translated:str = googleTranslator.translate(label.text.split('\n', 1)[0], dest='en').text.lower() # translate qs to en
            # handle languages questions : basic , good etc.. 
            if "english" in label_translated.lower():
                    LinkedinUtils.select_option(element, user.skills.languages.get_level("english")) 
            elif "german" in label_translated.lower():
                    LinkedinUtils.select_option(element, user.skills.languages.get_level("german")) 
            elif "experience" in label_translated.lower():
                LinkedinUtils.select_option(element, user.years_experience)
            elif "visa" in label_translated.lower():
                LinkedinUtils.select_option(element, user.visa_required)
            elif "how did you" in label_translated.lower():
                LinkedinUtils.select_option(element, "linkedin")
            # handle questions that can be answered by yes or no
            elif "do you" in label_translated.lower() or "have you" in label_translated.lower() or "are your" in label_translated.lower():
                LinkedinUtils.select_option(element, "yes")
            else:
                LinkedinUtils.select_option(element, "first")

        except:
            print(f"unable to process {qs_type}") 


    @staticmethod
    def process_checkbox_question( label:WebElement, elements: WebElement, user:CandidateProfile):
        qs_type= "checkbox question"
        googleTranslator = Translator()
        try:
            print("checkbox question: ", label.text.strip() )
            # if only one checkbox to click, just fucking click it if is not already clicked
            if len(elements) == 1:
                label = elements[0].find_element(By.TAG_NAME, "label")
                if not label.is_selected():
                    label.click()
                    print(f"element {elements[0].text} clicked successfully.")
                    return 
            for element in elements:
                #for opt_label in label_options:
                    print("checkbox option: ", element.text)
                    if element.text.lower() == googleTranslator.translate("I Agree Terms & Conditions", dest='en').text.lower():
                        label = element.find_element(By.TAG_NAME, "label")
                        if not label.is_selected():
                            label.click()
                            print(f"element {element.text} clicked successfully.")
                            return
        except Exception as e:
            print(f"unable to process {qs_type}") 

