from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re 

class JobDetailsExtractorLinkedin:
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
    
    def getJobID(self, element:WebElement):
        # extract job id 
        try:
            # Extract the job ID attribute value
            self.job_id = element.get_attribute('data-occludable-job-id')
            # Print the extracted job ID
            print("Job ID:", self.job_id)
            return self.job_id
        except Exception as e:
            print("Exception:", e)

    def getJobDescriptionText(self, element:WebElement):

        try:
            # Find the <div> element with the specified class and ID
            div_element = element.find_element(By.CSS_SELECTOR,'div.jobs-description-content__text#job-details')
            # Extract the text content of the <div> element
            content = div_element.text
            # Print the extracted content
            skip = "see link directly"
            print(f"Job Details: {skip}")
            #print(content)
            return skip
        except Exception as e:
            print("Exception:", e)

    def getCompanyEmails(self, element:WebElement):
        #find job title 
        try:
            # Find the <div> element with the specified class and ID
            div_element = element.find_element(By.CSS_SELECTOR,'div.jobs-description-content__text#job-details')
            # Extract the text content of the <div> element
            content = div_element.text
            # Use a regular expression to find email addresses
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            emails = re.findall(email_pattern, content)
            # Print the extracted email addresses
            print("Extracted Email Addresses:", emails)
            return emails
        except Exception as e:
            print("exception:", e)

    def getHiringManagerName(self, element:WebElement):
        #find job title 
        try:
            # Find the <span> element with the specified class
            span_element = element.find_element(By.CSS_SELECTOR,'span.jobs-poster__name.t-14.t-black.mb0')
            # Extract the text content of the <span> element
            poster_name = span_element.text.strip()
            # Print the extracted job poster's name
            print("Job Poster's Name:", poster_name)
            return poster_name
        except Exception as e:
            return None
