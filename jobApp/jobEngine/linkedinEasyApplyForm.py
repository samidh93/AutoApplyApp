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

''' use linkedin easy apply form template'''

class LinkedInEasyApplyForm(FormFillBase):
    def __init__(self, url=None, csv_links='jobApp/data/links.csv'):
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
                    links[1].append(row[4])  # extern links
        self.links = links

    def get_the_url(self, url=None):
        if url is None:
            url = self.url
        # navigate to the URL
        self.driver.get(url)

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
            in_apply = self.driver.find_element(
                By.XPATH, "//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.click()
        # if already applied
        except NoSuchElementException:
            print('You already applied to this job, go to next...')

    def applyForAllLinks(self):
        for link in self.links[1]:
            print(f"parsing link: {link}")
            self.get_the_url(link)
            self.clickApplyPage()
            while (1):
                pass
        
if __name__ == '__main__':
    easyApplyForm = LinkedInEasyApplyForm()
    easyApplyForm.applyForAllLinks()
