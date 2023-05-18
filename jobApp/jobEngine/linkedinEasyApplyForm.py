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

''' use linkedin easy apply form template'''

class LinkedInEasyApplyForm(FormFillBase ):
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
        self.driver.implicitly_wait(10)

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
            self.driver.get(url)
            self.status= True
        except:
            print("can't open link in the browser")
            self.status= False

    def fillFirstPage(self):
        # fill the expected first page template
        pass

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
            # Wait for the button to appear on the page
            wait = WebDriverWait(self.driver, 10)  # Maximum wait time of 10 seconds
            button = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='artdeco-button__text' and text()='Easy Apply']")))
            button.click()
        # if already applied
        except:
            print('easy apply job button is not found, skipping')
            self.status = False

    def applyForJob(self, job_link:str)->bool:
        # return true if job was success, false if job not found, deleted or can't apply
        self.get_the_url(job_link) # get the url form the job 
        self.clickApplyPage() # try to click
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
