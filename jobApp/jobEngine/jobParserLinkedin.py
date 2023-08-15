import json
import csv
import os
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin
from fileLocker import FileLocker
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from jobDataExtractorLinkedin import LinkedinJobDetailsExtractor

class JobParser:
    def __init__(self, linkedin_data, csv_links='jobApp/data/links.csv',  easyApply = False):
        """Parameter initialization"""
        with open(linkedin_data) as config_file:
            data = json.load(config_file)
        self.base_url = data["urls"]['search_job_url']
        self.page_num = data["params"]['pageNum']
        self.job_title = data["login"]['keywords']
        self.location = data["login"]['location']
        self.job_pos = data["params"]['start']
        self.filter_easy_apply = data["params"]['f_AL']
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'position': self.job_pos,  # 25 per page
            'pageNum': self.page_num,  # we increment this for next page
            'f_AL': self.filter_easy_apply  # we increment this for next page
        }
        # the bot
        self.bot = EasyApplyLinkedin('jobApp/secrets/linkedin.json', headless=True)
        self.csv_file = csv_links
        self.job_details_list = []

    def createListOfLinksDriver(self, page_to_visit, filter_links= True, save_html=True):
        # iterate all results and extract each job link
        self.bot.login_linkedin(True)
        sel_driver = self.bot.getEasyApplyJobSearchUrlResults()
        total_jobs = self.getTotalJobsSearchCount(sel_driver)
        total_pages = self.getAvailablesPages(sel_driver)
        if page_to_visit > total_pages:
            page_to_visit = total_pages # we can only extract availables opages
        job_index=0
        for _ in range(page_to_visit) : #skip first page, iterate until number of pages to visit
            job_list = self.getListOfJobsOnPage(sel_driver)
            # Print the list of extracted job titles
            print(f"number of jobs on this page: {len(job_list)}")
            for job in job_list:
                self.moveClickJob(sel_driver, job)
                job_index+=1
                print(f"current job index: {job_index}")
                job_details = self.getJobDetailsDict(sel_driver)
                self.job_details_list.append(job_details)
            time.sleep(1)
            sel_driver = self.bot.getEasyApplyJobSearchUrlResults(start=job_index)
            time.sleep(1)
        # save is not here
        self.writeDataToCsv(self.job_details_list, self.csv_file)
        return self.job_details_list

    def getJobDetailsDict(self, job: WebElement, driver: WebElement):
        jobDataExtractor = LinkedinJobDetailsExtractor()
        link = self.getJobLink(job)
        job_id = jobDataExtractor.getJobID(job)
        div_element = driver.find_element(By.CSS_SELECTOR,'div.scaffold-layout__detail.overflow-x-hidden.jobs-search__job-details')
        job_title= jobDataExtractor.getJobTitleSelenium(div_element)
        company= jobDataExtractor.getCompanySelenium(div_element)
        num_applicants= jobDataExtractor.getNumberApplicants(div_element)
        published= jobDataExtractor.getPublicationDate(div_element)
        job_details = {"job_id": job_id, "link": link, "title": job_title, "location": self.location, 
                       "company": company, "number_applicants": num_applicants, "date publication": published}
        return job_details

    def getJobLink(self, job: WebElement):
        try:
            link_element = WebDriverWait(job, 3).until(
            EC.presence_of_element_located((By.TAG_NAME, 'a')))
            link_href = link_element.get_attribute('href')
            return link_href
        except Exception as e:
            print("exception:", e)

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
        except Exception as e:
            print("exception:", e)
    
    def getListOfJobsOnPage(self, element: WebElement):
            # find jobs on page
        try:
            jobs_container = element.find_element(By.CLASS_NAME,"scaffold-layout__list-container")
            li_elements = jobs_container.find_elements(By.CSS_SELECTOR,'li[id^="ember"][class*="jobs-search-results__list-item"]')
            return li_elements
        except Exception as e:
            print("exception:", e)

    def moveClickJob(self, driver: WebElement, element:WebElement):
        # move the cursor to the job, click it to focus  
        try:
            hover = ActionChains(driver).move_to_element(element)
            hover.perform()
            element.click()
        except Exception as e:
            print("exception:", e)

    def writeDataToCsv(self, Data_in, Csv_file_out):
        # Write the dictionary to the CSV file
        with open(Csv_file_out, 'w', newline='') as file:
            fieldnames = Data_in[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row
            writer.writerows(Data_in)  # Write the data rows
        print(f"CSV file '{Csv_file_out}' created successfully.")

    def saveJobsDataToCsv(self, jobsDict, csv_file):
        # Check if the CSV file exists: read and append only new links
        flocker = FileLocker()
        ids = list()
        counter = 0
        if os.path.isfile(csv_file):
            # Read
            with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
                flocker.lockForRead(file)
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    ids.append(row[3])  # we get all ids there
                flocker.unlock(file)
            # write
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                flocker.lockForWrite(file)
                writer = csv.writer(file)
                for i, link in enumerate(jobsDict):  # new links loop
                    if link["job_id"] not in ids:
                        counter += 1
                        writer.writerow([len(ids)+counter,
                                         self.job_title,
                                         self.location,
                                         link["job_id"],
                                         link["link"]])
                flocker.unlock(file)
        # no csv, write new from zero
        else:
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                flocker.lockForWrite(file)
                writer = csv.writer(file)
                # Write the header row if the file is empty
                if os.stat(csv_file).st_size == 0:
                    writer.writerow(
                        ['id', 'keyword', 'location', 'job_id', 'link'])
                for i, link in enumerate(jobsDict):
                    writer.writerow([i+1,
                                     self.job_title,
                                     self.location,
                                     link["job_id"],
                                     link["link"]])
                flocker.unlock(file)
        print(f"Links saved to {csv_file}")


if __name__ == '__main__':

    jobParserObj = JobParser('jobApp/secrets/linkedin.json')
    jobParserObj.setEasyApplyFilter(False)
    jobsLinks = jobParserObj.generateLinksSeleniumV2()
