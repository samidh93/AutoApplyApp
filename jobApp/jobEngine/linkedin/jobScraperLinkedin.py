import csv
from .linkedinSeleniumBase import LinkedinSeleniumBase
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from .jobDataExtractorLinkedin import JobDetailsExtractorLinkedin
from ..job.job import Job
import threading
import os
from selenium import webdriver
from collections import deque
from ..utils.fileLocker import FileLocker
import concurrent.futures

class JobScraperLinkedin:
    def __init__(self, linkedin_data_file, csv_file_out='jobApp/data/jobs.csv',  application_type = "internal" or "external"):
        # the base class
        self.linkedin_data = linkedin_data_file
        self.linkedinObj = LinkedinSeleniumBase(linkedin_data_file)
        self.job_title = self.linkedinObj.job_title
        self.job_location = self.linkedinObj.location
        self.owner_id = self.linkedinObj.owner_id
        self.created_date = self.linkedinObj.created_date
        self.field_id = self.linkedinObj.field_id
        self.csv_file = csv_file_out
        self.job_details_list = deque()
        self.application_type = application_type

    def getJobCountFound(self):
        # login to get easy apply jobs
        self.linkedinObj.login_linkedin(True)
        # get the parametrized url search results
        self.driver = self.linkedinObj.getEasyApplyJobSearchRequestUrlResults()
        # wait 1 second to fully load results
        #time.sleep(1)
        self.total_jobs = self.getTotalJobsSearchCount(self.driver)
        return self.total_jobs

    def replace_spaces_and_commas_with_underscores(self, input_string:str):
        # Replace spaces and commas with underscores
        modified_string = input_string
        if " " in  input_string:
            modified_string = input_string.replace(' ', '_')
        elif "," in input_string:
            modified_string = input_string.replace(',', '_')
        return modified_string
    
    def createFileJobLocation(self):
        csv_file_out_without_extension = self.csv_file[:-4]
        job_title = self.replace_spaces_and_commas_with_underscores(self.job_title)
        location = self.replace_spaces_and_commas_with_underscores(self.job_location)
        csv_extension = ".csv"
        file = csv_file_out_without_extension+"_"+job_title+"_"+location+"_"+self.field_id+csv_extension # maybe owner id is needed here
        return file

    def isJobApplied(self, job: WebElement):
        try:
            applied:WebElement = job.find_element(By.CSS_SELECTOR, "ul.job-card-list__footer-wrapper li.job-card-container__footer-item strong span.tvm__text--neutral")
            if "Applied" in applied.text:
                print("skipping already applied job")
                return True
        except:
            print("job not applied, extracting job data")
            return False

    def processPage(self, page_number,total_pages,  page_cookies):
        print(f"visiting page number {page_number}, remaining pages {total_pages - page_number}")
        driver = self.driver
        if page_number>0:
            linkedinObj = LinkedinSeleniumBase(self.linkedin_data)
            linkedinObj.saved_cookies = page_cookies
            driver = linkedinObj.getEasyApplyJobSearchRequestUrlResults(start=page_number*25)
        job_list = self.getListOfJobsOnPage(driver)
        # Print the list of extracted job titles
        job_index = page_number*25
        print(f"number of jobs on this page: {len(job_list)}")
        for job in job_list:
            if self.isJobApplied(job=job):
                continue
            # we incrementn here to track only valid jobs
            job_index+=1 
            self.moveClickJob(driver, job)
            print(f"current job index: {job_index}")
            jobObj = self.createJobObj(job_index, job, driver)
            self.job_details_list.append(jobObj.to_dict())
            self.writeJobToCsv(jobObj.to_dict(),self.createFileJobLocation() )

    def saveJobsList(self, page_to_visit):
        total_pages = self.getAvailablesPages(self.driver) or 1
        if page_to_visit > total_pages:
            page_to_visit = total_pages  # we can only extract available pages
        print(f"number of pages available to parse: {page_to_visit}")
        # Create a ThreadPoolExecutor with a specified number of threads
        num_threads = 5  # You can adjust the number of threads based on your system's capabilities
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for p in range(page_to_visit):  # skip first page, iterate until the number of pages to visit
                # Submit the page processing tasks to the ThreadPoolExecutor
                futures.append(executor.submit(self.processPage, p,page_to_visit, self.linkedinObj.saved_cookies))
            # Wait for all submitted tasks to complete
            concurrent.futures.wait(futures)
        
        return self.job_details_list
    
    def collectJobsThreads(self, page_to_visit):
        # Create and start the first thread
        thread1 = threading.Thread(target=self.getJobCountFound)
        thread1.start()
        # Wait for the first thread to finish
        thread1.join()
        # Create and start the second thread (background thread)
        thread2 = threading.Thread(target=self.saveJobsList,args=[page_to_visit], daemon=True)
        thread2.start()

    def createJobObj(self, index: int, job: WebElement, driver: webdriver.Chrome)->Job:
        jobDataExtractor = JobDetailsExtractorLinkedin()
        link = self.getJobLink(job, driver)
        job_id = jobDataExtractor.getJobID(job)
        div_element = driver.find_element(By.CSS_SELECTOR,'div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details')
        job_title= jobDataExtractor.getJobTitleSelenium(div_element)
        company= jobDataExtractor.getCompanySelenium(div_element)
        num_applicants= jobDataExtractor.getNumberApplicants(div_element)
        published= jobDataExtractor.getPublicationDate(div_element)
        job_description = jobDataExtractor.getJobDescriptionText(div_element)
        emails = jobDataExtractor.getCompanyEmails(div_element)
        poster_name = jobDataExtractor.getHiringManagerName(div_element)
        applied = False
        job = Job(id=index,  job_id=job_id,  link=link, job_title=job_title, job_location= self.job_location, company_name=company,num_applicants= num_applicants, posted_date=published,
                 job_description=job_description, company_emails=emails, job_poster_name=poster_name, application_type=self.application_type, applied=applied )
        return job


    def getJobLink(self, job: WebElement, driver:webdriver.Chrome):
        try:
            link_element:WebElement = WebDriverWait(job, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'a')))
            link_href = link_element.get_attribute('href')
            print("extracted job link: ", link_href)
            return link_href
        except NoSuchElementException as e:
            print("job link extraction error:", e)

    def getTotalJobsSearchCount(self, element: WebElement):
       # find the total amount of results 
        try:
            total_results = element.find_element(
                By.CLASS_NAME, "jobs-search-results-list__subtitle")
            total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", "").replace(".", "").replace("+",""))
            print(f"total jobs found: {total_results_int}")
            return total_results_int
        except NoSuchElementException:
            print("no results found ")

    def getAvailablesPages(self, element: WebElement):
        ## find pages availables
        try:
            list_pages = element.find_element(
                    By.XPATH, '//ul[contains(@class, "artdeco-pagination__pages--number")]')
            list_pages_availables = list_pages.find_elements(By.TAG_NAME, 'li' )
            last_li = list_pages_availables[-1]
            last_p = last_li.get_attribute("data-test-pagination-page-btn")
            pages_availables = int(last_p)
            print(f"total pages availables: {pages_availables}")
            return pages_availables
        except:
            print("exception available pages occured")
    
    def getListOfJobsOnPage(self, driver: webdriver.Chrome):
            # find jobs on page
        try:
            time.sleep(5)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__list-container"))
            )
            jobs_container = driver.find_element(By.CLASS_NAME,"scaffold-layout__list-container")
            li_elements = jobs_container.find_elements(By.CSS_SELECTOR,"li[class*='jobs-search-results__list-item']")
            return li_elements
        except:
            print("exception list jobs occured")

    def moveClickJob(self, driver: WebElement, element:WebElement):
        # move the cursor to the job, click it to focus  
        try:
            hover = ActionChains(driver).move_to_element(element)
            hover.perform()
            element.click()
        except:
            print("exception click job occured")

    def writeDataToCsv(self, Data_in, Csv_file_out):
        # Write the dictionary to the CSV file
        with open(Csv_file_out, 'w', newline='') as file:
            fieldnames = Data_in[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            writer.writerows(Data_in)  # Write the data rows
        print(f"CSV file '{Csv_file_out}' created successfully.")

    def writeJobToCsv(self, Job:dict, Csv_file_out):
        # Check if the file exists
        flocker = FileLocker()
        file_exists = os.path.exists(Csv_file_out)

        # Open the CSV file in append mode
        with open(Csv_file_out, 'a', newline='') as file:
            flocker.lockForWrite(file)
            fieldnames = Job.keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # If the file doesn't exist, write the header row
            if not file_exists:
                writer.writeheader()  # Write the header row
            writer.writerow(Job)  # Write the data row
            print(f"CSV file '{Csv_file_out}' updated successfully.")
            flocker.unlock(file)

if __name__ == '__main__':
    pass