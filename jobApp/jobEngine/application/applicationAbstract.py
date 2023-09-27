from ..email.gmail import Gmail
from ..user.candidateProfile import CandidateProfile
from ..job.job import Job
import csv
from abc import ABC, abstractmethod
import os
from ..utils.fileLocker import FileLocker
import threading
from ..config.config import UserConfig, AppConfig

def print_progress_bar(iteration, total, bar_length=50):
    percent = "{:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    print(f"Progress: [{bar}] {percent}% Complete", end="\r")

class Application(ABC):
    def __init__(self, candidate: CandidateProfile, jobOffers:list[Job], csvJobsFile=UserConfig.get_jobs_file_path()) -> None:
        self.candidate_profile = candidate
        self.jobs = jobOffers
        self.csv_file = csvJobsFile
        if csvJobsFile:
            print("loading jobs from file directly")
            self.load_jobs_from_csv()

    @abstractmethod
    def ApplyForJob(self, job:Job):
        pass

    # add thread for each job application
    def ApplyForAll(self, application_type = "internal" or "external", application_limit=10):
        threads = [threading.Thread] #list of threeads
        print("applying for jobs from the csv file")          
        for i,j in enumerate(self.jobs):
            print_progress_bar(i, len(self.jobs)+1)
            if j.applied:
            # we already applied for this job
                continue
            #print(f"application filter type: {application_type}, current job application type: {j.application_type}")
            if application_type == j.application_type: # apply for the same type
                print(f"\n################ applying for job number {j.id} ##################\n")
                #thread = threading.Thread(target=self.ApplyForJob, args=(j,))
                #thread.daemon = True
                #thread.start()
                #threads.append(thread)
                self.ApplyForJob(j)
            else:
                print(f"ignoring {j.application_type} ")
                continue
        # Wait for all threads to finish
        #for thread in threads:
        #    print(f"runnig thread")
        #    thread.join(self)   
        print("\nApplying Task completed!")
        self.update_csv() # after finish, update 

    def load_jobs_from_csv(self):
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
        self.jobs = jobs

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
    