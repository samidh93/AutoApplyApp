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

def print_progress_bar(completed_jobs, total_jobs, bar_length=50):
    percent = "{:.1f}".format(100 * (completed_jobs / float(total_jobs)))
    filled_length = int(bar_length * completed_jobs // total_jobs)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    print(f"Progress: [{bar}] {percent}% Complete", end="\r")

class Application(ABC):
    def __init__(self, candidate: CandidateProfile, csvJobsFile=BaseConfig.get_data_path(), linkedin_data=None) -> None:
        self.linkedin_data = linkedin_data
        self.candidate_profile = candidate
        self.csv_file = csvJobsFile
        self.jobs = self.load_jobs_from_csv()
        self.lock = threading.Lock()  # Create a lock for thread-safe progress updates

    @abstractmethod
    def ApplyForJob(self, job:Job,  cookies:list):
        pass

    def set_linkedin_data(self, linkedin_data):
        self.linkedin_data = linkedin_data

    def ApplyForAll(self, application_type="internal" or "external", application_limit=10):
        print("applying for jobs from the csv file")
        #self.jobs = self.jobs[:10]
        print("candidate applications limit: ", application_limit)
        self.get_applied_jobs_count()
        print("number of applied jobs found: ", self.jobs_applied)
        print("remainig jobs to apply for: ", len(self.jobs)- self.jobs_applied)
        # login task here
        baseObj = LinkedinSeleniumBase(self.linkedin_data)
        log_driver = baseObj.login_linkedin(save_cookies=True)
        self.cookies = baseObj.saved_cookies
        log_driver.quit()
        # Create a ThreadPoolExecutor with a specified number of threads
        num_threads = 4  # we keep only 4 due to some issues
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            self.completed_jobs = 0  # To keep track of completed jobs
            futures = []
            for i, j in enumerate(self.jobs):
                if j.applied:
                    # we already applied for this job
                    print(f"skipping applied job: {j.job_id}")
                    continue
                if application_type == j.application_type:
                    #print(f"\n################ applying for job number {j.id} ##################\n")
                    self.candidate_profile.generate_summary_for_job(job_title=j.job_title, company=j.company_name, platform=j.platform, hiring_manager=j.job_poster_name)
                    # Submit the job application task to the ThreadPoolExecutor
                    futures.append(executor.submit(self.ApplyForJob, j, self.cookies))
                else:
                    print(f"Ignoring {j.application_type}")
                    continue
            # Wait for all submitted tasks to complete
            concurrent.futures.wait(futures)
        print("\nApplying Task completed!")
#    # add thread for each job application
#    def ApplyForAll(self, application_type = "internal" or "external", application_limit=10):
#        print("applying for jobs from the csv file") 
#        print("candidate applications limit: ", application_limit)         
#        for i,j in enumerate(self.jobs):
#            print_progress_bar(i, len(self.jobs)+1)
#            if j.applied:
#            # we already applied for this job
#                continue
#            if application_type == j.application_type: # apply for the same type
#                print(f"\n################ applying for job number {j.id} ##################\n")
#                self.candidate_profile.generate_summary_for_job(job_title=j.job_title, company=j.company_name, platform=j.platform, hiring_manager=j.job_poster_name)
#                self.ApplyForJob(j)
#                self.update_job_status(j)
#            else:
#                print(f"ignoring {j.application_type} ")
#                continue
#        print("\nApplying Task completed!")
#
    def load_jobs_from_csv(self)->list[Job]:
        flocker = FileLocker()
        jobs = [] #list of jobs
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, "r", newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
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
        print("updating jobs in csv file")
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

        print("Updating job status in CSV file")

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
        
    def get_applied_jobs_count(self):
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
                print("Error while processing the file:", e)
            finally:
                flocker.unlock(file)
