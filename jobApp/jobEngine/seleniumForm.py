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


class SeleniumFormHandler(FormFillBase):
    def __init__(self, form_json_template='jobApp/secrets/form.json', url=None, csv_links='jobApp/data/links.csv'):
        super().__init__(form_json_template, url)

        # get the absolute path of the current working directory
        self.cwd = os.getcwd()
        # dict {"what": [css, by]}
        self.fields_css_dict = {
            "firstname": ['input[{}*=first]', "name"], "lastname": ['input[{}*=last]', "name"],
            "fullname": ['input[{}*=full]', "name"], "telephone": ['input[{}*=tel]', "type"],
            "email": ['input[{}*=email]', "type"], "cv":  ['input[{}*="file"][name*="cv"]', "type"],
            "submit": ['button[{}*=submit]', "type"]
        }
        self.fields_object_references = {
            "firstname": None, "lastname": None,
            "fullname": None, "telephone": None,
            "email": None, "cv":  None,
            "submit": None
        }
        self.fields_candidate = {
            "firstname": "zayneb", "lastname": "dhieb",
            "fullname": "zayneb dhieb", "telephone": "+21620094923",
            "email": "dhiebzayneb89@gmail.com", "cv":  f"{self.cwd}/jobApp/data/zayneb_dhieb_resume_english.pdf",
        }

        self.links = []
        self.csv_file = csv_links
        if csv_links:
            print("loading links from file directly")
            self.load_links_from_csv()

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
    # get the URL of the current page
    def get_all_input_fields(self):
        input_fields = self.driver.find_elements(By.TAG_NAME, 'input')
        for field in input_fields:
            if field.get_attribute('type') == "hidden":
                continue
            print(f"form_input_field_name: {field.get_attribute('name')}")
            print(f"form_input_field_type: {field.get_attribute('type')}")
            print(f"form_input_field_id: {field.get_attribute('id')}")
            print(f"form_input_field_value: {field.get_attribute('value')}")
            print(f"-------------------------------------------------------")


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

    def fillInField(self, element, value):
        element.clear()
        # time.sleep(1)
        element.send_keys(value)

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

    def runAllLinks(self):
        for link in self.links[1]:
            print(f"parsing link: {link}")
            formHandle.get_the_url(link)
            formHandle.get_all_input_fields()
            #formHandle.find_all_input_fields()
            #formHandle.autofill()
            #formHandle.submit()
            while (1):
                pass


if __name__ == '__main__':
    formHandle = SeleniumFormHandler()
    formHandle.runAllLinks()
