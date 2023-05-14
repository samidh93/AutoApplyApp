from bs4 import BeautifulSoup
import json
import requests
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin
from selenium import webdriver
from selenium.webdriver.common.by import By
from formFillBase import FormFillBase
import os
import time
import csv
from googletrans import Translator
import os
from google.cloud import translate_v2 as translate
from coverCreator import CoverCreator

class Field:
    def __init__(self, field_element, input_elements: list) -> None:
        self.field_element = field_element
        self.elements_list = input_elements


class SeleniumFormHandler(FormFillBase):
    def __init__(self, form_json_template='jobApp/secrets/form.json', url=None, csv_links='jobApp/data/links.csv'):
        super().__init__(form_json_template, url)
        # Set up credentials and API client
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'jobApp/secrets/credentials_sami.json'
        self.translator = translate.Client.from_service_account_json(
            'jobApp/secrets/translator_key.json')
        # get the absolute path of the current working directon
        self.cwd = os.getcwd()
        # dict {"what": [css, by]}
        self.fields_css_dict = {
            "firstname": ['input[{}*=first]', "name"], "lastname": ['input[{}*=last]', "name"],
            "fullname": ['input[{}*=full]', "name"], "phone": ['input[{}*=tel]', "type"],
            "email": ['input[{}*=email]', "type"], "cv":  ['input[{}*="file"][name*="cv"]', "type"],
            "submit": ['button[{}*=submit]', "type"]
        }
        self.fields_object_references = {
            "firstname": None, "lastname": None,
            "fullname": None, "phone": None,
            "email": None, "cv":  None,
            "submit": None
        }
        data = ["project manager", "stroomrecruitment", "zayneb dhieb", "+21620094923" ]

        self.fields_candidate = {
            "firstname": "zayneb",
            "lastname": "dhieb",
            "fullname": "zayneb dhieb",
            "phone": "+21620094923",
            "email": "dhiebzayneb89@gmail.com",
            "cv":  f"{self.cwd}/jobApp/data/zayneb_dhieb_resume_english.pdf",
            "bio": CoverCreator(candidate_infos=data)()
        }
        self.links = []
        self.csv_file = csv_links
        if csv_links:
            print("loading links from file directly")
            self.load_links_from_csv()

        # List of possible first name field names in English
        self.first_name_fields = {"firstname": [
            'firstname', 'first name']}
        self.last_name_fields = {"lastname": [
            'lastname', 'last name']}
        self.full_name_fields = {"fullname": [
            'fullname', 'full name']}
        self.email_fields = {
            "email": ['email']}
        self.phone_fields = {"phone": [
            'phone', 'tel', "phone number", "mobile"]}
        self.cv_fields = {"cv": ['cv', 'resume', 'file']}
        self.bio_fields = {"bio": ['about', 'report', 'summary', 'message']}
        #self.submit_field = {"submit": ["submit", "send", "apply"]}
        self.search_keywords = [self.first_name_fields, self.last_name_fields,
                                self.full_name_fields, self.email_fields, self.phone_fields, self.cv_fields, self.bio_fields]
        self.fields_obj_list = []
        self.pair_to_send = []

###########################################################
################### FORM API V2 ###########################
###########################################################

    def load_links_from_csv(self):
        links = [[], [], []]  # list of 2 lists
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for i, row in enumerate(reader):
                    links[1].append(row[5])  # extern links
        self.links = links

    def get_the_url(self, url=None):
        if url is None:
            url = self.url
        # navigate to the URL
        self.driver.get(url)

    def get_all_input_fields(self):
        # get all input fields
        try:
            self.form = self.driver.find_element(By.TAG_NAME, 'form')
        except:
            print("No form found")
            return -1
        textareas = self.form.find_elements(By.TAG_NAME, 'textarea')
        try:
            input_fields = self.form.find_elements(By.TAG_NAME, 'input')
        except:
            print("No input fields found")
            return -1 
        if len(input_fields)<5: # detect unkown form
            return -1      
        if len(textareas)>0: # we have text areas to fill
            input_fields.extend(textareas)
        print("parsing form fields")
        for field in input_fields:
            # Get the attributes of the field
            try:
                field_name = field.get_attribute('name')
            except:
                print("field has no attribute name")
                field_name = None
            try:
                field_id = field.get_attribute('id')
            except:
                print("field has no attribute id")
                field_id = None
            try:
                field_type = field.get_attribute('type')
            except:
                print("field has no attribute type")
                field_type = None
            try:            
                field_value = field.get_attribute('value')
            except:
                print("field has no attribute value")
                field_value = None
            if field_type == "hidden":
                continue
            print(f"form_input_field_name: {field_name}")
            print(f"form_input_field_type: {field_type}")
            print(f"form_input_field_id: {field_id}")
            print(f"form_input_field_value: {field_value}")
            print(f"-------------------------------------------------------")
            # Detect the language of the field name
            # Translate the field name to English if it is not already in English
            if self.field_lang_detect_translate(field_name) != field_name and self.field_lang_detect_translate(field_name) != None:
                field_name = self.field_lang_detect_translate(field_name)
                print(f"translated field_name: {field_name}")
            if self.field_lang_detect_translate(field_type) != field_type and self.field_lang_detect_translate(field_type) != None:
                field_type = self.field_lang_detect_translate(field_type)
                print(f"translated field_type: {field_type}")
            if self.field_lang_detect_translate(field_id) != field_id and self.field_lang_detect_translate(field_id) != None:
                field_id = self.field_lang_detect_translate(field_id)
                print(f"translated field_id: {field_id}")
            if self.field_lang_detect_translate(field_value) != field_value and self.field_lang_detect_translate(field_value) != None:
                field_value = self.field_lang_detect_translate(field_value)
                print(f"translated field_value: {field_value}")
            print(f"-------------------------------------------------------")
            self.fields_obj_list.append(
                Field(field, [field_name, field_type, field_id, field_value]))
        return 0

    # Detect the language of the field and translate to en if not
    def field_lang_detect_translate(self, field_attr):
        # If the input word is already in English, return it
        if field_attr == "":
            return None
        lang = self.translator.detect_language(field_attr)
        if lang is None:
            print("unkown language")
            return None
        if lang['language'] != 'en':
            print(f"non english field detected {field_attr}")
            return self.translator.translate(field_attr, target_language='en')['translatedText']
        return field_attr

    def search_list_of_dicts(self, lst, search_str):
        if search_str == None or search_str == "" or search_str == " ":
            return False, None, None
        for d in lst:
            for k, v in d.items():
                if isinstance(v, list):
                    if any(search_str in s for s in v):
                        return True, k, v
                else:
                    if search_str in v:
                        return True, k, v
        return False,  None, None

    def create_match_pair_input_field_user_input(self):
        # match a field class with search and create a pair if found
        # iterate the full list of fields (obj)
        for input_field in self.fields_obj_list:
            for input_element in input_field.elements_list:  # iterate the 4 elements: name, type, id , value
                # search nested list of dictfor input element
                found, k, v = self.search_list_of_dicts(
                    self.search_keywords, input_element)
                if found:
                    print(
                        f"Found input element '{input_element}' in dict with key '{k}' in '{v}'.")
                    self.create_pair(input_field.field_element, k)
                    # found element in search keywords
                    break

    def create_pair(self, input_field, key) -> dict:
        self.pair_to_send.append(
            {"input_field": input_field, "val_to_send": self.fields_candidate[key]})
        print(
            f"creating pair: '{input_field}' object and value to send '{self.fields_candidate[key]}'")

    def fillInField(self, input_field, user_value):
        #input_field.clear()
        # time.sleep(1)
        input_field.send_keys(user_value)

    def send_input_fields_user_values(self):
        # iterate the list of input fields and send the user values
        for pair in self.pair_to_send:
            self.fillInField(pair['input_field'], pair['val_to_send'])

    def submit_form(self):
        self.form.submit()

    def runAllLinks(self):
        for link in self.links[1]:
            print(f"parsing link: {link}")
            self.get_the_url(link)
            if self.get_all_input_fields() <0:
                continue
            self.create_match_pair_input_field_user_input()
            self.send_input_fields_user_values()
            #self.submit_form()
            
            while (1):
                pass
#################################################################
#################### Form API V1: deprecated, use V2 instead ################################
#################################################################

    def find_field_by_css(self, key, field_css: list):
        try:
            field = self.driver.find_element(
                By.CSS_SELECTOR, field_css[0].format(field_css[1]))
            if field:
                self.fields_object_references[key] = field
                print(f"found key {key}: ")
                print(field.get_attribute(field_css[1]))
                return True
        except:
            print("element not found exception")

    def find_all_input_fields(self):
        for key, value in self.fields_css_dict.items():
            # use case: firstname and lastname found: ignore fullname
            found = self.find_field_by_css(key, value)
        print(len(self.fields_object_references))

    def submit(self):
        try:
            self.fields_object_references["submit"].submit()
        except:
            print("submit failed")

    def search_nested_list(self, nested_list, search_string):
        for sublist in nested_list:
            for string in sublist:
                if search_string in string:
                    return True,
        return False

    def autofill(self):
        for key, webelement in self.fields_object_references.items():
            print(f"webelement: {webelement.get_attribute('value')}")
            if key == 'fullname':
                if webelement.get_attribute('value') != 'fullname':
                    continue
            if key == 'submit':
                break
            if webelement is not None:
                self.fillInField(webelement, self.fields_candidate[key])


if __name__ == '__main__':
    formHandle = SeleniumFormHandler()
    formHandle.runAllLinks()
