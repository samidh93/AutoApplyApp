from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re 

class LinkedinJobDetailsExtractor:

    def __init__(self):
        pass

   ####### use selenium ####
    def getJobTitleSelenium(self, element: WebElement):
        #find job title 
        try:
            title= element.find_element(By.CSS_SELECTOR,'h2.t-24.t-bold.jobs-unified-top-card__job-title')
            self.extracted_title = title.text
            print(f"job title: {self.extracted_title}")
            return self.extracted_title 
        except Exception as e:
            print("exception:", e)

    def getCompanySelenium(self, element: WebElement):
        #find company title 
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.jobs-unified-top-card__primary-description')
            company=  div_element.find_element(By.CSS_SELECTOR,"a.app-aware-link")
            self.extracted_company = company.text
            print(f"company: {self.extracted_company}")
            return self.extracted_company
        except Exception as e:
            print("exception:", e)

    def getLocationSelenium(self, element: WebElement):
        #find job title 
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.jobs-unified-top-card__primary-description')
            # try via html source code: already given in the search bar: skipping here
            print(f"location: {self.extracted_location}")
            return self.extracted_location
        except Exception as e:
            print("exception:", e)

    def getNumberApplicants(self, element:WebElement):
        #find job title 
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.jobs-unified-top-card__primary-description')
            try:
                applicants=  div_element.find_element(By.CSS_SELECTOR,'span.tvm__text--positive')
                self.num_applicants = applicants.text
            except:
                applicants=  div_element.find_elements(By.CSS_SELECTOR,'span.tvm__text--neutral')
                self.num_applicants = applicants[-1].text
            print(f"num_applicants: {self.num_applicants}")
            return self.num_applicants
        except Exception as e:
            print("exception:", e)

    def getPublicationDate(self, element:WebElement):
        #find job title 
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.jobs-unified-top-card__primary-description')
            date=  div_element.find_elements(By.CSS_SELECTOR,'span.tvm__text--neutral')
            self.publish_date = date[0].text
            print(f"publish_date: {self.publish_date}")
            return self.publish_date
        except Exception as e:
            print("exception:", e)
