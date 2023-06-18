from bs4 import BeautifulSoup
import json
import requests
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
import os
import time
import csv
from formFillBase import FormFillBase
from seleniumWrapper import WebScraper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumForm import Field, SeleniumFormHandler

''' use linkedin easy apply form template'''

class LinkedInEasyApplyForm( SeleniumFormHandler ):
    def __init__(self, url=None, csv_links='jobApp/data/links.csv'):
        self.links = []
        self.csv_file = csv_links
        super().__init__(url=url)
        if csv_links:
            print("loading links from file directly")
            self.load_links_from_csv()
        scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
        bot = scraper.createJobSearchSession()
        self.driver = bot.driver # pass the new driver to current one
        #self.driver.implicitly_wait(20)

    def load_links_from_csv(self):
        # load only onsite links
        links = []  # list of intern lists
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for i, row in enumerate(reader):
                    if row[5] == "None": # append only easy apply links
                        links.append(row[4])  # intern links
        self.links = links
        print(f"onsite apply links count: {len(links)}")

    def get_the_url(self, url=None):
        if url is None:
            url = self.url
        # navigate to the URL
        try: # try to open link in browser
                        # Open a new window and switch to it
            #self.driver.execute_script("window.open('','_blank');")
            #self.driver.switch_to.window(self.driver.window_handles[1])
            #print("opening job link in new tab")
            #self.driver.execute_script("window.open(arguments[0], '_blank');", url)
            self.driver.get(url)
            #self.status= True
            #self.driver.switch_to.window(self.driver.window_handles[0])
            #self.driver.quit()
        except:
            print("can't open link in the browser")
            self.status= False

    def clickApplyPage(self):
        # click on the easy apply button, skip if already applied to the position
        time.sleep(1)
        try:
            print("try clicking button easy apply")
            # Wait for the button element to be clickable
            button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
            )
            #button = self.driver.find_element(By.XPATH, "//span[@class='artdeco-button__text' and text()='Easy Apply']")
            button.click()
            print("button apply clicked")
        # if already applied or not found
        except:
            print('easy apply job button is not found, skipping')
            self.status = False

    def _find_form_first_page(self):
  # fill the expected first page template
        try:
            div_element = self.driver.find_element(By.CSS_SELECTOR, 'div.artdeco-modal.artdeco-modal--layer-default.jobs-easy-apply-modal')
            if div_element:
                # Find the form element within the div
                form_element = div_element.find_element(By.TAG_NAME, 'form')
                if form_element:
                    print(f"form_element found: form object {form_element}")
                    self.form  = form_element # pass the form to parent
                else:
                    # The form element was not found within the div
                    print('Form element not found')
            else:
                # The div element was not found
                print('Div element not found')
        except:
            print("no page found")

    def fillFirstPage(self):
        self._find_form_first_page() # try to find the form
        if self.form != None: # if form is found 
            # Find all divs within the form
            # Find the div with class "jobs-easy-apply-form-section__grouping"
            divs = self.form.find_elements(By.CSS_SELECTOR, 'div.jobs-easy-apply-form-section__grouping')
            # Iterate over the divs and extract the label and corresponding input/select values
            for div in divs:
                label_element = div.find_element(By.TAG_NAME, 'label')
                label = label_element.text.strip()
                print(f"Label: {label}")
                try:
                    input_element = div.find_element(By.TAG_NAME, 'input')
                    value = input_element.get_attribute('value').strip()
                    print(f"Input Value: {value}")
                except:
                    select_element = div.find_element(By.TAG_NAME, 'select')
                    options = select_element.find_elements(By.TAG_NAME, 'option')
                    value = [option.get_attribute('value').strip() for option in options]
                    print(f"Select Options: {value}")

    def fillSecondPage(self):
        # fill the expected second page template
        pass

    def fillOptionsSelectPage(self):
        # fill the expected options select page template
        pass

    def clickNextPage(self):
        # click the next page button
        pass

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
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply')]"))
            )
            #button = self.driver.find_element(By.XPATH, "//span[@class='artdeco-button__text' and text()='Easy Apply']")
            button.click()
            print("button apply clicked")
        # if already applied or not found
        except:
            print('easy apply job button is not found, skipping')
            self.status = False

    def applyForJob(self, job_link:str)->bool:
        # return true if job was success, false if job not found, deleted or can't apply
        self.get_the_url(job_link) # get the url form the job 
        self.clickApplyPage() # try to click
        self.fillFirstPage() # detect form and fill first page

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
