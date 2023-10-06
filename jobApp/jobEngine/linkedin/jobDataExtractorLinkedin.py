from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re 

class JobDetailsExtractorLinkedin:
    def __init__(self):
        pass

   ####### use selenium ####
    def getJobTitleSelenium(self, element: WebElement):
        #find job title 
        what_data = "job title"
        try:
            title= element.find_element(By.CSS_SELECTOR,'h2.t-24.t-bold.job-details-jobs-unified-top-card__job-title')
            self.extracted_title = title.text
            print(f"job title: {self.extracted_title}")
            return self.extracted_title 
        except:
            print(f"exceptionn occured while extracting job data: {what_data}")

    def getCompanySelenium(self, element: WebElement):
        #find company title 
        what_data = "company name"
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.job-details-jobs-unified-top-card__primary-description')
            company=  div_element.find_element(By.CSS_SELECTOR,"a.app-aware-link")
            self.extracted_company = company.text
            print(f"company: {self.extracted_company}")
            return self.extracted_company
        except:
            print(f"exceptionn occured while extracting job data: {what_data}")

    def getLocationSelenium(self, element: WebElement):
        #find job title 
        what_data = "location"
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.job-details-jobs-unified-top-card__primary-description')
            # try via html source code: already given in the search bar: skipping here
            print(f"location: {self.extracted_location}")
            return self.extracted_location
        except:
            print(f"exceptionn occured while extracting job data: {what_data}")

    def getNumberApplicants(self, element:WebElement):
        #find job title 
        what_data = "num of applicants"
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.job-details-jobs-unified-top-card__primary-description')
            try:
                applicants=  div_element.find_element(By.CSS_SELECTOR,'span.tvm__text--positive')
                self.num_applicants = applicants.text
            except:
                applicants=  div_element.find_elements(By.CSS_SELECTOR,'span.tvm__text--neutral')
                self.num_applicants = applicants[-1].text
            print(f"num_applicants: {self.num_applicants}")
            return self.num_applicants
        except:
            print(f"exceptionn occured while extracting job data: {what_data}")

    def getPublicationDate(self, element:WebElement):
        #find job title 
        what_data = "publication date"
        try:
            div_element = element.find_element(By.CSS_SELECTOR,'div.job-details-jobs-unified-top-card__primary-description')
            date=  div_element.find_elements(By.CSS_SELECTOR,'span.tvm__text--neutral')
            self.publish_date = date[0].text
            print(f"publish_date: {self.publish_date}")
            return self.publish_date
        except:
            print(f"exceptionn occured while extracting job data: {what_data}")
    
    def getJobID(self, element:WebElement):
        # extract job id 
        what_data = "job id"
        try:
            # Extract the job ID attribute value
            self.job_id = element.get_attribute('data-occludable-job-id')
            # Print the extracted job ID
            print("Job ID:", self.job_id)
            return self.job_id
        except:
            print(f"Exceptionn occured while extracting job data: {what_data}")

    def getJobDescriptionText(self, element:WebElement):

        what_data = "job description"
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
        except:
            print(f"Exceptionn occured while extracting job data: {what_data}")

    def getCompanyEmails(self, element:WebElement):
        #find job title 
        what_data = "company emails"
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
        except:
            print(f"exceptionn occured while extracting job data: {what_data}")

    def getHiringManagerName(self, element:WebElement):
        #find job title 
        what_data = "hiring manager"
        try:
            # Find the <span> element with the specified class
            span_element = element.find_element(By.CSS_SELECTOR,'span.jobs-poster__name.t-14.t-black.mb0')
            # Extract the text content of the <span> element
            poster_name = span_element.text.strip()
            # Print the extracted job poster's name
            print("Job Poster's Name:", poster_name)
            return poster_name
        except:
            print(f"exceptionn occured while extracting job data: {what_data}")
            return None
