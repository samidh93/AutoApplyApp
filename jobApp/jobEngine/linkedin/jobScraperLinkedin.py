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
    def __init__(self, linkedin_data_file, csv_file_out='jobApp/data/jobs.csv',  application_type="internal" or "external"):
        # the base class
        self.linkedin_data = linkedin_data_file
        self.linkedinObj = LinkedinSeleniumBase(linkedin_data_file)
        self.job_title = self.linkedinObj.job_title
        self.job_location = self.linkedinObj.location
        self.owner_id = self.linkedinObj.owner_id
        self.created_date = self.linkedinObj.created_date
        self.field_id = self.linkedinObj.field_id
        self.application_limit = int(self.linkedinObj.applications_limit)
        self.csv_file = csv_file_out
        self.job_details_list = deque()
        self.application_type = application_type
        self.global_job_index_lock = threading.Lock()
        self.job_handler_lock = threading.Lock()
        self.global_job_index = 0  # track the global job index, used for determing the limit
        self.job_index_list = []
        self.limit_reached_event = threading.Event()
        self.page_threads = 1  # import to calculate overload of running more than one page thread
        self.job_threads = 1  # import to calculate overload of running more than one job thread

    def getJobCountFound(self):
        # login to get easy apply jobs
        self.linkedinObj.login_linkedin(True)
        # get the parametrized url search results
        self.driver = self.linkedinObj.getEasyApplyJobSearchRequestUrlResults()
        # wait 1 second to fully load results
        # time.sleep(1)
        self.total_jobs = self.getTotalJobsSearchCount(self.driver)
        return self.total_jobs

    def replace_spaces_and_commas_with_underscores(self, input_string: str):
        # Replace spaces and commas with underscores
        modified_string = input_string
        if " " in input_string:
            modified_string = input_string.replace(' ', '_')
        elif "," in input_string:
            modified_string = input_string.replace(',', '_')
        return modified_string

    def createFileJobLocation(self):
        csv_file_out_without_extension = self.csv_file[:-4]
        job_title = self.replace_spaces_and_commas_with_underscores(
            self.job_title)
        location = self.replace_spaces_and_commas_with_underscores(
            self.job_location)
        csv_extension = ".csv"
        file = csv_file_out_without_extension+"_"+job_title+"_"+location + \
            "_"+self.field_id+csv_extension  # maybe owner id is needed here
        return file

    def isJobApplied(self, job: WebElement):
        try:
            applied: WebElement = job.find_element(
                By.CSS_SELECTOR, "ul.job-card-list__footer-wrapper li.job-card-container__footer-item strong span.tvm__text--neutral")
            if "Applied" in applied.text:
                print("skipping already applied job")
                return True
        except:
            print("job not applied, extracting job data")
            return False

    def processJob(self, job: WebElement, page):
        thread_id = threading.current_thread().name
        if self.limit_reached_event.is_set():
            print(f"limit reached return current job thread: {thread_id}")
            return
        print(f"Current Job Thread Name: {thread_id}")
        if self.isJobApplied(job=job):
            return
        with self.global_job_index_lock:
            # increment to global job index
            self.global_job_index += 1
            # 25 = 25+1, 
            self.job_index_list[page] = self.job_index_list[page] +1 #+ page*25
            print(f"global job index tracker: {self.global_job_index}")
            if self.global_job_index >= self.application_limit:
                self.limit_reached_event.set()
                print("limit reached, set event to all threads..")
            print(f"current job index: {self.job_index_list[page]}")
            jobObj = self.createJobObj(self.job_index_list[page], job)
        # thread safe
        self.job_details_list.append(jobObj.to_dict())
        self.writeJobToCsv(jobObj.to_dict(), self.createFileJobLocation())
        # we lock shared variables for write /read

    def processPage(self, page_number, total_pages,  page_cookies):
        thread_id = threading.get_ident()
        if self.limit_reached_event.is_set():
            print(f"limit reached return current page thread: {thread_id}")
            return
        print(
            f"visiting page number {page_number}, remaining pages {total_pages - page_number-1}")
        print(f"Current Page Thread ID: {threading.current_thread().name}")
        driver = self.driver
        if page_number > 0:
            linkedinObj = LinkedinSeleniumBase(self.linkedin_data)
            linkedinObj.saved_cookies = page_cookies
            driver = linkedinObj.getEasyApplyJobSearchRequestUrlResults(
                start=page_number*25)
        job_list = self.getListOfJobsOnPage(driver)
        # Print the list of extracted job titles
        print(f"number of jobs on this page: {len(job_list)}")
        # Create a ThreadPoolExecutor with a maximum number of threads
        prefix = f"page_{page_number}_job"
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.job_threads, thread_name_prefix=prefix) as executor:
            futures = []
            for i, job in enumerate(job_list):
                if self.limit_reached_event.is_set():
                    print("limit reached breaking job loop")
                    break
                # 25
                if i%self.job_threads == 0:
                    print("current job loop index: ", i)
                    with self.job_handler_lock:
                        self.moveClickJob(driver, job)
                futures.append(executor.submit(
                    self.processJob, job, page_number))
            # Wait for all submitted tasks to complete
            concurrent.futures.wait(fs=futures, return_when="FIRST_COMPLETED")
        print(f"finishing page thread: {thread_id}")
        driver.quit()

    def saveJobsList(self, page_to_visit=5): # max of 125 jobs: need to be calculated based on applications_limit
        start_time = time.time()
        total_pages = self.getAvailablesPages(self.driver) or 1
        jobs_per_page = 25
        # assume the number of pages: (app_limit)/25 + 1, we add extra one
        page_to_visit = (self.application_limit // jobs_per_page) + (2 if self.application_limit % jobs_per_page > 0 else 1) 
        #page_to_visit = int(self.application_limit/jobs_per_page) + 1
        if page_to_visit > total_pages:
            page_to_visit = total_pages
        print(f"number of pages available to visit: {page_to_visit}")
        print(f"number of applications limited by user: {self.application_limit}")
        # to be sure we are in the limit of pages
        self.page_threads = page_to_visit
        # need more investigation how driver handles threads, for now 2 seems to be ok
        self.job_threads = 2
        self.job_index_list = [i * jobs_per_page for i in range(page_to_visit)]
        # Create a ThreadPoolExecutor with a specified number of threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.page_threads) as executor:
            futures = []
            # skip first page, iterate until the number of pages to visit
            for p in range(page_to_visit):
                if self.limit_reached_event.is_set():
                    print("limit reached breaking page loop")
                    break
                # Submit the page processing tasks to the ThreadPoolExecutor
                futures.append(executor.submit(
                    self.processPage, p, page_to_visit, self.linkedinObj.saved_cookies))
            # Wait for all submitted tasks to complete
            concurrent.futures.wait(fs=futures, return_when="FIRST_COMPLETED")

        self.job_details_list = self.sort_deque_by_id_ascending(
            'id', self.job_details_list)
        # sort data ascending by id: index
        self.writeDataToCsv(self.job_details_list,
                            self.createFileJobLocation())
        end_time = time.time() - start_time
        print(f"job scraping took {end_time} seconds")
        return self.job_details_list

    def collectJobsThreads(self, page_to_visit):
        # Create and start the first thread
        thread1 = threading.Thread(target=self.getJobCountFound)
        thread1.start()
        # Wait for the first thread to finish
        thread1.join()
        # Create and start the second thread (background thread)
        thread2 = threading.Thread(target=self.saveJobsList, args=[
                                   page_to_visit], daemon=True)
        thread2.start()

    def extractJobData(self, job: WebElement, jobDataExtractorObj:  JobDetailsExtractorLinkedin):
        div_element = job.find_element(
            By.CSS_SELECTOR, 'div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details')
        job_title = jobDataExtractorObj.getJobTitleSelenium(div_element)
        company = jobDataExtractorObj.getCompanySelenium(div_element)
        num_applicants = jobDataExtractorObj.getNumberApplicants(div_element)
        published = jobDataExtractorObj.getPublicationDate(div_element)
        job_description = jobDataExtractorObj.getJobDescriptionText(
            div_element)
        emails = jobDataExtractorObj.getCompanyEmails(div_element)
        poster_name = jobDataExtractorObj.getHiringManagerName(div_element)

    def createJobObj(self, index: int, job: WebElement) -> Job:
        try:
            jobDataExtractor = JobDetailsExtractorLinkedin(job)
            jobDataExtractor.getJobLink(job)
            jobDataExtractor.getJobID(job)
            # use it when to extract all details, otherwise details will be None
            # self.extractJobData(job,jobDataExtractor )
            applied = False
            job = Job(id=index, job_id=jobDataExtractor.job_id, link=jobDataExtractor.job_link,
                      job_title=jobDataExtractor.job_title, job_location=self.job_location,
                      company_name=jobDataExtractor.company, num_applicants=jobDataExtractor.num_applicants,
                      posted_date=jobDataExtractor.published, job_description=jobDataExtractor.job_description,
                      company_emails=jobDataExtractor.emails, job_poster_name=jobDataExtractor.hiring_manager,
                      application_type=self.application_type, applied=applied)
            return job
        except:
            print("error creating job obj")

    def getTotalJobsSearchCount(self, element: WebElement):
       # find the total amount of results
        try:
            total_results = element.find_element(
                By.CLASS_NAME, "jobs-search-results-list__subtitle")
            total_results_int = int(total_results.text.split(
                ' ', 1)[0].replace(",", "").replace(".", "").replace("+", ""))
            print(f"total jobs found: {total_results_int}")
            return total_results_int
        except NoSuchElementException:
            print("no results found ")

    def getAvailablesPages(self, element: WebElement):
        # find pages availables
        try:
            list_pages = element.find_element(
                By.XPATH, '//ul[contains(@class, "artdeco-pagination__pages--number")]')
            list_pages_availables = list_pages.find_elements(By.TAG_NAME, 'li')
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
            time.sleep(1)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "scaffold-layout__list-container"))
            )
            jobs_container = driver.find_element(
                By.CLASS_NAME, "scaffold-layout__list-container")
            li_elements = jobs_container.find_elements(
                By.CSS_SELECTOR, "li[class*='jobs-search-results__list-item']")
            return li_elements
        except:
            print("exception list jobs occured")

    def moveClickJob(self, driver: WebElement, job: WebElement):
        # move the cursor to the job, click it to focus
        try:
            print(
                f"moving to next job from thread: {threading.current_thread().name}")
            hover = ActionChains(driver).move_to_element(job)
            hover.perform()
            job.click()
        except:
            print("exception move to job occured")

    def writeDataToCsv(self, Data_in, Csv_file_out):
        # Write the dictionary to the CSV file
        with open(Csv_file_out, 'w', newline='') as file:
            fieldnames = Data_in[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            writer.writerows(Data_in)  # Write the data rows
        print(f"CSV file '{Csv_file_out}' created successfully.")

    def sort_deque_by_id_ascending(self, sort_filter, input_deque):
        # Use sorted() with a custom key function to sort the deque
        sorted_deque = deque(
            sorted(input_deque, key=lambda item: item[sort_filter]))
        return sorted_deque

    def sortDataByIndexCsv(self, csvToSort):
        # Read the CSV data and sort by 'id' in ascending order
        with open(csvToSort, 'r', newline='') as file:
            reader = csv.DictReader(file)
            sorted_data = sorted(reader, key=lambda row: int(row['id']))

        # Write the sorted data back to the CSV file
        with open(csvToSort, 'w', newline='') as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write the header row
            writer.writeheader()

            # Write the sorted rows
            for row in sorted_data:
                writer.writerow(row)

        print(f"CSV file '{csvToSort}' sorted successfully.")

    def writeJobToCsv(self, Job: dict, Csv_file_out):
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
