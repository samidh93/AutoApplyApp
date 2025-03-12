from ..email.gmail import Gmail
from ..user.candidateProfile import CandidateProfile
from ..job.job import Job
import csv
from abc import ABC, abstractmethod
import os
from ..utils.fileLocker import FileLocker
import threading
from ..config.config import BaseConfig, UserConfig, AppConfig
import concurrent.futures
import os
import multiprocessing
from selenium import webdriver
from ..linkedin.linkedinSeleniumBase import LinkedinSeleniumBase
import queue
import time
import json
import logging
logger = logging.getLogger(__name__)

def print_progress_bar(completed_jobs, total_jobs, bar_length=50):
    percent = "{:.1f}".format(100 * (completed_jobs / float(total_jobs)))
    filled_length = int(bar_length * completed_jobs // total_jobs)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    logger.info(f" Progress: [{bar}] {percent}% Complete Jobs")

class Application(ABC):
    def __init__(self, candidate: CandidateProfile, csvJobsFile=BaseConfig.get_data_path(), linkedin_data=None) -> None:
        self.linkedin_data = linkedin_data
        self.candidate_profile = candidate
        self.csv_file = csvJobsFile
        self.jobs = self.load_jobs_from_csv()
        self.lock = threading.Lock()  # Create a lock for thread-safe progress updates
        self.limit_reached_event = threading.Event()
        self.max_browsers= 1
        self.completed_jobs = 0  # To keep track of completed jobs
        self.success_jobs = 0

    @abstractmethod
    def ApplyForJob(self, job:Job,  cookies:list):
        pass

    def set_linkedin_data(self, linkedin_data):
        self.linkedin_data = linkedin_data

    def get_applied_jobs(self):
        pass 

    def get_jobs_to_apply_count(self , application_limit):
        logger.info("applying for jobs from the csv file")
        #self.jobs = self.jobs[:10]
        self.application_limit = int(application_limit)
        logger.info("candidate applications limit: %d", self.application_limit)
        logger.info("number of jobs to apply for: %s", len(self.jobs))
        return len(self.jobs)

    def executeJobsMultiThreaded(self, application_type="internal", application_limit=100):
    # login task here
        start_time = time.time()
        baseObj = LinkedinSeleniumBase(self.linkedin_data)
        log_driver = baseObj.login_linkedin(save_cookies=True)
        self.cookies = baseObj.saved_cookies
        log_driver.quit()
        futures = []
        # Create a ThreadPoolExecutor with a specified number of threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_browsers) as executor:
            for i, j in enumerate(self.jobs):
                if self.limit_reached_event.is_set():
                    logger.info("application limit reached breaking job loop")
                    break
                if j.applied:
                    # we already applied for this job
                    logger.info(f"skipping applied job: {j.job_id}")
                    continue
                if application_type == j.application_type:
                    logger.info(f"\n################ applying for job number {j.id} ##################\n")
                    self.candidate_profile.set_current_job(job=j)
                    # Submit the job application task to the ThreadPoolExecutor
                    futures.append(executor.submit(self.ApplyForJob, j, self.cookies))
                else:
                    logger.info(f"Ignoring {j.application_type}")
                    continue
            # Wait for all submitted tasks to complete
            concurrent.futures.wait(futures)
        logger.info(":::::::::Applying Task completed!:::::::::")
        end_time = time.time() - start_time
        logger.info(f"job apply service took: {end_time} seconds")
        #return succefull jobs
        self.success_jobs = [job.to_dict() for job in self.jobs if job.applied]
        #logger.info(f"succeded job dict: {self.success_jobs}")
        self.save_applied_jobs_file(self.success_jobs, UserConfig.get_jobs_result_json_path(self.csv_file))
        return self.success_jobs

    def executeJobs(self, application_type="internal", application_limit=100):
    # login task here
        start_time = time.time()
        baseObj = LinkedinSeleniumBase(self.linkedin_data)
        log_driver = baseObj.login_linkedin(save_cookies=True)
        self.cookies = baseObj.saved_cookies
        log_driver.quit()
        # Create a ThreadPoolExecutor with a specified number of threads
        for i, j in enumerate(self.jobs):
            if self.limit_reached_event.is_set():
                logger.info("application limit reached breaking job loop")
                break
            if j.applied:
                # we already applied for this job
                logger.info(f"skipping applied job: {j.job_id}")
                continue
            if application_type == j.application_type:
                logger.info(f"\n################ applying for job number {j.id} ##################\n")
                logger.info(f"\n################ job link {j.link} ##################\n")
                self.candidate_profile.set_current_job(job=j)
                # Submit the job application task to the ThreadPoolExecutor
                self.ApplyForJob(j, self.cookies)
            else:
                logger.info(f"Ignoring {j.application_type}")
                continue

        logger.info(":::::::::Applying Task completed!:::::::::")
        end_time = time.time() - start_time
        logger.info(f"job apply service took: {end_time} seconds")
        #return succefull jobs
        self.success_jobs = [job.to_dict() for job in self.jobs if job.applied]
        #logger.info(f"succeded job dict: {self.success_jobs}")
        self.save_applied_jobs_file(self.success_jobs, UserConfig.get_jobs_result_json_path(self.csv_file))
        return self.success_jobs
    
    # use multihtreading context for incoming request
    def ApplyForAllMultiThreaded(self, application_type="internal" or "external", application_limit=100):
        # Create and start the first thread
        #thread1 = threading.Thread(target=self.get_jobs_to_apply_count,  args=[
        #                           application_limit],)
        #thread1.start()
        ## Wait for the first thread to finish
        #thread1.join()
        # Create and start the second thread (background thread)
        self.application_limit = int(application_limit)
        logger.info("candidate applications limit: %d", self.application_limit)
        thread2 = threading.Thread(target=self.executeJobs, args=[
                                   application_type, application_limit], daemon=False)
        thread2.start()
        thread2.join()

    # use multihtreading context for incoming request
    def ApplyForAll(self, application_type="internal" or "external", application_limit=100):
        self.application_limit = int(application_limit)
        jobs = self.executeJobs(application_type, application_limit)

    def load_jobs_from_csv(self)->list[Job]:
        flocker = FileLocker()
        jobs = [] #list of jobs
        logger.info(f"file:: {self.csv_file}")
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, "r", newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row["applied"] == "False":
                        job = Job(
                            id=row["id"],
                            job_id=row["job_id"],
                            link=row["link"],
                            job_title=row["job_title"],
                            job_location=row["job_location"],
                            company_name=row["company_name"],
                            num_applicants=row["num_applicants"],
                            posted_date=row["posted_date"],
                            job_description=row["job_description"],
                            company_emails=row["company_emails"],
                            job_poster_name=row["job_poster_name"],
                            application_type=row["application_type"],
                            applied=row["applied"] == "True"
                        )
                        jobs.append(job)
                flocker.unlock(file)
        return jobs


    def update_csv(self):
        flocker = FileLocker()
        logger.info("updating jobs in csv file")
        with open(self.csv_file, mode='r',newline='',  encoding='utf-8' ) as file:
            flocker.lockForRead(file)
            reader = csv.DictReader(file)
            job_data = [row for row in reader]
            flocker.unlock(file)

        for job in self.jobs:
            for row in job_data:
                if row['job_id'] == str(job.job_id):
                    row['applied'] = job.applied

        with open(self.csv_file, mode='w',newline='',  encoding='utf-8' ) as file:
            flocker.lockForWrite(file)
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(job_data)
            flocker.unlock(file)


    def update_job_status(self, job: Job):
        flocker = FileLocker()
        logger.info("Updating job status in CSV file")
        # Open the file for reading
        with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
            flocker.lockForRead(file)
            reader = csv.DictReader(file)
            job_data = [row for row in reader]

        # Perform updates on job_data
        for row in job_data:
            if row['job_id'] == str(job.job_id):
                row['applied'] = job.applied

        # Reopen the file for writing
        with open(self.csv_file, mode='w', newline='', encoding='utf-8') as file:
            flocker.lockForWrite(file)
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(job_data)
            # Unlock the file after writing
            flocker.unlock(file)

    def save_applied_jobs_file(self, jobs: list[dict], result_file: str):
        flocker = FileLocker()
        try:
            # Create a dictionary to store the data in the desired format
            data = {
                "job_count": len(jobs),
                "jobs": jobs
            }
            # Write the data to the JSON file
            with open(result_file, 'w') as json_file:
                flocker.lockForWrite(json_file)
                json.dump(data, json_file, indent=4)  # Indent for pretty printing
                flocker.unlock(json_file)
            logging.info(f"Saved job data to {result_file}")
        except Exception as e:
            logging.error(f"Error while saving job data: {e}")
            # Handle the error or raise an exception as needed


    def get_applied_jobs_count_file(self):
        flocker = FileLocker()
        self.jobs_applied = 0
        # Open the file for reading
        with open(self.csv_file, mode='r', newline='', encoding='utf-8') as file:
            flocker.lockForRead(file)
            try:
                reader = csv.DictReader(file)
                job_data = [row for row in reader]

                # Perform updates on job_data
                for row in job_data:
                    if row['applied'] == 'True':  # Note: 'True' is a string, not a boolean
                        self.jobs_applied += 1
            except Exception as e:
                logger.error("Error while processing the file: %s", e)
            finally:
                flocker.unlock(file)
