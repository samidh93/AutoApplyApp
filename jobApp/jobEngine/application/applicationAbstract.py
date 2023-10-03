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

def print_progress_bar(iteration, total, bar_length=50):
    percent = "{:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    print(f"Progress: [{bar}] {percent}% Complete", end="\r")

class Application(ABC):
    def __init__(self, candidate: CandidateProfile, csvJobsFile=BaseConfig.get_data_path()) -> None:
        self.candidate_profile = candidate
        self.csv_file = csvJobsFile
        self.jobs = self.load_jobs_from_csv()

    @abstractmethod
    def ApplyForJob(self, job:Job):
        pass

    def ApplyForAll(self, application_type="internal" or "external", application_limit=10):
        print("applying for jobs from the csv file")
        print("candidate applications limit: ", application_limit)

        # Create a ThreadPoolExecutor with a specified number of threads
        num_threads = os.cpu_count()  # You can adjust this based on your system's capabilities
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []

            for i, j in enumerate(self.jobs):
                print_progress_bar(i, len(self.jobs) + 1)
                if j.applied:
                    # We already applied for this job
                    continue

                if application_type == j.application_type:
                    print(f"\n################ applying for job number {j.id} ##################\n")
                    self.candidate_profile.generate_summary_for_job(job_title=j.job_title, company=j.company_name, platform=j.platform, hiring_manager=j.job_poster_name)
                    # Submit the job application task to the ThreadPoolExecutor
                    futures.append(executor.submit(self.ApplyForJob, j))
                    futures.append(executor.submit(self.update_job_status, j))

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
    
    def update_job_status(self, job:Job):
        flocker = FileLocker()
        print("updating job status in csv file")
        with open(self.csv_file, mode='w',newline='',  encoding='utf-8' ) as file:
            flocker.lockForWrite(file)
            reader = csv.DictReader(file)
            job_data = [row for row in reader]
            flocker.unlock(file)
            for row in job_data:
                if row['job_id'] == str(job.job_id):
                    row['applied'] = job.applied