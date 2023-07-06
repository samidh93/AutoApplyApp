from bs4 import BeautifulSoup
import json
import requests
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
import os
import time
import csv
from formFillBase import FormFillBase
from seleniumWrapper import WebScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumForm import Field, SeleniumFormHandler
from selenium.webdriver.support.ui import Select
from candidateProfile import CandidateProfile
from collections.abc import Iterable


''' use linkedin easy apply form template'''


class LinkedInEasyApplyForm(SeleniumFormHandler):
    def __init__(self, candidate_profile: CandidateProfile, url=None, csv_links='jobApp/data/links.csv'):
        self.links = []
        self.csv_file = csv_links
        super().__init__(url=url)
        if csv_links:
            print("loading links from file directly")
            self.load_links_from_csv()
        scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
        bot = scraper.createJobSearchSession()
        self.driver = bot.driver  # pass the new driver to current one
        self.label_elements_map = {}
        self.candidate = candidate_profile
        self.button_apply_clicked = False

        # self.driver.implicitly_wait(20)

    def load_links_from_csv(self):
        # load only onsite links
        links = []  # list of intern lists
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for i, row in enumerate(reader):
                    if row[5] == "None":  # append only easy apply links
                        links.append(row[4])  # intern links
        self.links = links
        print(f"onsite apply links count: {len(links)}")

    def get_the_url(self, url=None):
        if url is None:
            url = self.url
        # navigate to the URL
        try:  # try to open link in browser
            # Open a new window and switch to it
            # self.driver.execute_script("window.open('','_blank');")
            # self.driver.switch_to.window(self.driver.window_handles[1])
            # print("opening job link in new tab")
            # self.driver.execute_script("window.open(arguments[0], '_blank');", url)
            self.driver.get(url)
            # self.status= True
            # self.driver.switch_to.window(self.driver.window_handles[0])
            # self.driver.quit()
        except:
            print("can't open link in the browser")
            self.status = False

    def clickApplyPage(self):
        # click on the easy apply button, skip if already applied to the position
        try:
            print("try clicking button easy apply")
            # Wait for the button element to be clickable
            button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
            )
            # button = self.driver.find_element(By.XPATH, "//span[@class='artdeco-button__text' and text()='Easy Apply']")
            button.click()
            self.button_apply_clicked = True
            print("button apply clicked")

            # if already applied or not found
        except:
            print('easy apply job button is not found, retry..')
            self.status = False

    def _find_form_first_page(self):
      # fill the expected first page template
        try:
            self.div_element_form_holder = self.driver.find_element(
                By.CSS_SELECTOR, 'div.artdeco-modal.artdeco-modal--layer-default.jobs-easy-apply-modal')
            if self.div_element_form_holder:
                # Find the form element within the div
                form_element = self.div_element_form_holder.find_element(
                    By.TAG_NAME, 'form')
                if form_element:
                    print(f"form_element found: form object {form_element}")
                    self.form = form_element  # pass the form to parent
                else:
                    # The form element was not found within the div
                    print('Form element not found')
            else:
                # The div element was not found
                print('Div element not found')
        except:
            print("no page found")

    def _send_user_details(self, user: CandidateProfile, elements_dict: dict[WebElement]):
        for label, element in elements_dict.items():
            if label == 'First name':
                self.send_value(element, user.firstname)
            elif label == 'Last name':
                self.send_value(element, user.lastname)
            elif label == 'Phone country code':
                self.select_option(element, user.phone_code)
            elif label == 'Mobile phone number':
                self.send_value(element, user.phone_number)
            elif label == 'Email address':
                self.select_option(element, user.email)
            elif label == 'Upload resume':
                self.send_value(element, user.resume.file_path)
            else:
                raise ValueError("Unsupported label: {}".format(label))

    def send_value(self, element: WebElement, value: str):
        element_type = element.get_attribute("type")
        if element_type == "file":
            print("The web element is a file input.")
            print(f"sending file path: {value}")
            element.send_keys(value)
        elif element_type == "text":
            element.clear()
            element.send_keys(value)
        else:
            print("input type not recognized")

    def select_option(self, select_element, user_value):
        select = Select(select_element)
        if isinstance(select.options, Iterable):
            if user_value in select.options:
                select.select_by_visible_text(user_value)
            else:  # return first option to bypass error; needed to be corrected
                select.select_by_visible_text(
                    select.first_selected_option.text)
            return
        else:
            select.select_by_visible_text(select.first_selected_option.text)

    def _find_divs_document_upload(self) -> list[WebElement]:
        if self.form != None:  # if form is found
            try:
                div_elements = self.form.find_elements(
                    By.XPATH, "//div[contains(@class, 'js-jobs-document-upload__container') and contains(@class, 'display-flex') and contains(@class, 'flex-wrap')]")
                return div_elements
            except NoSuchElementException:
                print("No div elements found")

    def _find_divs_selection_grouping(self) -> list[WebElement]:
        if self.form != None:  # if form is found
            try:
                # Find the div with class "jobs-easy-apply-form-section__grouping"
                divs = self.form.find_elements(
                    By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
                return divs
            except NoSuchElementException:
                print("No div elements found")

    def _createDictFromFormDiv(self, divs:  list[WebElement]):
        # Iterate over the divs and extract the label and corresponding input/select values
        for div in divs:
            label_element = div.find_element(By.TAG_NAME, 'label')
            label = label_element.text.strip()
            print(f"Label: {label}")
            try:
                input_element = div.find_element(By.TAG_NAME, 'input')
                value = input_element.get_attribute('value').strip()
                print(f"Input Value: {value}")
                # assign label with input elem object
                self.label_elements_map[label] = input_element
            except:
                select_element = div.find_element(By.TAG_NAME, 'select')
                # Create a Select object
                # select = Select(select_element)
                # assign label with select elem object
                self.label_elements_map[label] = select_element
        # Iterate over the dictionary
        for key in self.label_elements_map:
            value = self.label_elements_map[key]
            print(f"Key: {key}, Value: {value}")

    def fillFirstPage(self):
        self._find_form_first_page()  # try to find the form
        divs = self._find_divs_selection_grouping()
        if len(divs) != 0:
            # create the key,value pair for each element on the form
            self._createDictFromFormDiv(divs)
            # fill the form with candidate data
            self._send_user_details(self.candidate, self.label_elements_map)
            # click next buttton
            self._clickNextPage(self.form)

    def fillSecondPage(self):
        self._find_form_first_page()  # try to find the form
        divs = self._find_divs_document_upload()
        if len(divs) != 0:
            # create the key,value pair for each element on the form
            self._createDictFromFormDiv(divs)
            # fill the form with candidate data
            self._send_user_details(self.candidate, self.label_elements_map)
            # click next buttton
            self._clickNextPage(self.form)

    def fillOptionsSelectPage(self):
        # fill the expected options select page template
        pass

    def _clickNextPage(self, form: WebElement):
        # click the next page button
        # Find the button using its aria-label attribute
        try:
            button = form.find_element(By.XPATH, "//span[text()='Next']")

            #   "button[aria-label='Continue to next step']"
            # Click the button
            button.click()
        except:
            print("next button not found")

    def clickReviewPage(self):
        # click the review page button
        pass

    def clickSubmitPage(self):
        # click the submit page button
        pass

    def clickApplyPage(self):
        # click on the easy apply button, skip if already applied to the position
        try:
            print("try clicking button easy apply")
            # Wait for the button element to be clickable
            button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
            )
            # button = self.driver.find_element(By.XPATH, "//span[@class='artdeco-button__text' and text()='Easy Apply']")
            button.click()
            print("button apply clicked")
        # if already applied or not found
        except:
            print('easy apply job button is not found, skipping')
            self.status = False

    def applyForJob(self, job_link: str) -> bool:
        # return true if job was success, false if job not found, deleted or can't apply
        self.get_the_url(job_link)  # get the url form the job
        
        self.clickApplyPage()  # try to click apply button: retry when not clicked
        if not self.button_apply_clicked:
            time.sleep(3)
            self.clickApplyPage()
        self.fillFirstPage()  # detect form and fill first page
        self.label_elements_map.clear()
        self.fillSecondPage()  # fill second page

        return False

    def applyForAllLinks(self):
        for link in self.links:
            print(f"parsing link: {link}")
            self.get_the_url(link)
            self.clickApplyPage()
        while (1):
            pass


if __name__ == '__main__':
    easyApplyForm = LinkedInEasyApplyForm()
    easyApplyForm.applyForAllLinks()
