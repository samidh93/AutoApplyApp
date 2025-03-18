from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import csv
import time
from ..job.job import Job
from ..user.candidateProfile import CandidateProfile
from collections.abc import Iterable
from .jobsAttachSessionToLoginLinkedin import JobSearchRequestSessionAttachLinkedin
from .linkedinSeleniumBase import LinkedinSeleniumBase
from .linkedinFormButtonAbstract import ButtonFactory, Button
from ..resume.resumeGenerator import ResumeGenerator

''' handle linkedin easy apply form template'''
import logging
logger = logging.getLogger(__name__)

class LinkedInEasyApplyFormHandler:
    def __init__(self, candidate_profile: CandidateProfile, csv_jobs='jobApp/data/jobs.csv', linkedin_data_file='jobApp/secrets/linkedin.json'):
        self.csv_file = csv_jobs
        self.links = self.load_links_from_csv()
        self.label_elements_map = {}
        self.candidate = candidate_profile
        self.button_apply_clicked = False

    ###### Apply Phase #####
    def applyForJob(self, job:Job, driver: webdriver, cookies, use_timeout=False, timeout=900) -> bool:
        # keep track of the time for application, do not exceed max 3 minutes:
        self.cookies = cookies
        start_time = None
        if use_timeout == True:
            start_time = time.time()  # begin counter
            elapsed_time = time.time() - start_time  # Calculate elapsed time in seconds
            if elapsed_time >= timeout:  # 180 seconds = 3 minutes
               logger.info(f"Time limit {timeout} seconds per application exceeded. Returning from applyForJob.")
               return False
        # open job url
        self.get_the_url(job.link, driver)  # get the url form the job
        # return true if job was success or already applied
        if self.is_application_submitted(driver):
            return True
        # continue if is not submitted
        # wait for the click button to appear
        if not self.clickApplyPage(driver):
            return False
        # return false if button is not clicked
        if job.company_name == None or job.company_name == "":
            logger.info("company name is not found")
            element = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__company-name")
            company_name = element.text
            logger.info(f"company name: {company_name}")
            job.company_name = company_name
        # generate the resume for this job
        resume_gen = ResumeGenerator(job.link)
        resume_gen.run(self.candidate.firstname, self.candidate.lastname)
        # get the resume path
        self.candidate.resume=resume_gen.get_resume(self.candidate.firstname, self.candidate.lastname, job.company_name)
        self.candidate.formfiller.set_job(job)
        self.candidate.formfiller.set_user_context(resume_gen.get_resume_content(self.candidate.firstname, self.candidate.lastname,job.company_name ))
        # find the form
        form = self.find_application_form(driver)
        # handle form page
        if not self.handleFormPage(form, start_time, driver=driver, timeout=timeout):
            # error during apply job
            return False
        # return job applied true
        return True

    ####### Detect PAge #############
    def handleFormPage(self, form: WebElement, start_time=None, driver: webdriver = None, timeout=900):
        if start_time != None:
            # start_time = time.time()  # Record the start time
            elapsed_time = time.time() - start_time  # Calculate elapsed time in seconds
            if elapsed_time >= timeout:  # 180 seconds = 3 minutes
                logger.warning(f"Time limit {timeout} seconds per job app exceeded. quitting ..")
                return False
        buttonfactory = ButtonFactory()
        try:
            button: Button = buttonfactory.create_button(
                form, driver, self.candidate)
            button.fillSection(form)
            button.click()
            # submit exit condition
            if button.submitted:
                logger.info("form submitted succefully")
                return True
            return self.handleFormPage(form, start_time, driver=driver)
        except ValueError as E:
            logger.error("error: ", str(E))
            return False

    ###### load links from csv file ########
    def load_links_from_csv(self):
        # load only onsite links
        links = []  # list of intern lists
        if os.path.isfile(self.csv_file):
            logger.info("loading links from input jobs file: %s", self.csv_file)
            # Read
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for i, row in enumerate(reader):
                    links.append(row[2])  # intern links
        self.links = links
        logger.info(f"onsite apply links count: {len(links)}")

    ###### get url in browser #######
    def get_the_url(self, url, driver: webdriver):
        # navigate to the URL
        try:  # try to open link in browser
            driver.get(url)
            for cookie in self.cookies:
                driver.add_cookie(cookie)
            driver.refresh()
        except:
            logger.info("can't open link in the browser")
            self.status = False

    ###### find application form #########
    def find_application_form(self,  driver: webdriver):
      # fill the expected first page template
        try:
            self.div_element_form_holder = driver.find_element(
                By.CSS_SELECTOR, 'div.artdeco-modal.artdeco-modal--layer-default.jobs-easy-apply-modal')
            if self.div_element_form_holder:
                # Find the form element within the div
                form_element = self.div_element_form_holder.find_element(
                    By.TAG_NAME, 'form')
                if form_element:
                    # logger.info(f"form_element found: form object {form_element}")
                    self.form = form_element  # pass the form to parent
                    return form_element
                else:
                    # The form element was not found within the div
                    logger.info('Form element not found')
            else:
                # The div element was not found
                logger.info('Div element not found')
        except:
            logger.info("no page found")

    ####### Click Button Apply #########
    def clickApplyPage(self, driver: webdriver.Chrome):
        # click on the easy apply button, skip if already applied to the position
        try:
            # simulate click to interact
            logger.info("try clicking button easy apply")
            # Wait for the button element to be clickable
            button: WebElement = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "jobs-apply-button--top-card"))
            )
            button.click()
            self.button_apply_clicked = True
            logger.info("button easy apply clicked")
            return True
        # if already applied or not found
        except:
            logger.info('easy apply job button is not found, skipping')
            self.status = False


####### helper functions ########

    def is_application_submitted(self, driver: webdriver) -> bool:
        # click on the easy apply button, skip if already applied to the position
        try:
            # Wait for the timeline entries to load
            submitted = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[aria-label="Download your submitted resume"]')))
            logger.info(submitted.text.lower())
            if 'submitted resume' in submitted.text.lower():
                logger.info("application submitted")
                self.resume_submitted = True
                return True
        except:
            logger.info("submitted entry not found")
            return False

    def is_applications_closed(self, driver: webdriver):
        try:
            # Wait for the error element to load
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'jobs-details-top-card__apply-error')))
            error_element = driver.find_element(
                By.CLASS_NAME, 'jobs-details-top-card__apply-error')
            error_message = error_element.find_element(
                By.CLASS_NAME, 'artdeco-inline-feedback__message').text.strip()
            if "No longer accepting applications" in error_message:
                logger.info("application closed, no longer accepting applicants")
                return True
        except:
            return False


if __name__ == '__main__':
    pass
