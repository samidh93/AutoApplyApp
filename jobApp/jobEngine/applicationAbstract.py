from gmail import Gmail
from candidateProfile import CandidateProfile, ChatGPT
from jobBuilderLinkedin import JobBuilder, JobParser, Job
import csv
from abc import ABC, abstractmethod
import os
from fileLocker import FileLocker
class Application(ABC):
    def __init__(self, candidate: CandidateProfile, jobOffers:list[Job], csvJobsFile='jobApp/data/jobs.csv') -> None:
        self.candidate_profile = candidate
        self.jobs = jobOffers
        self.csv_file=csvJobsFile
        if csvJobsFile:
            print("loading jobs from file directly")
            self.load_jobs_from_csv()

    @abstractmethod
    def ApplyForJob(self, job:Job):
        pass
 
    def ApplyForAll(self):
        for j in self.jobs:
            self.ApplyForJob(j)
        self.update_csv() # after finish, update 

    def load_jobs_from_csv(self):
        flocker = FileLocker()
        jobs = [] #list of jobs
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, mode='r', newline='',  encoding='utf-8') as file:
                flocker.lockForRead(file)
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    applied = True if row[8].lower() == 'true' else False
                    if applied == True:
                        print("already applied for job")
                        continue #ignore job
                    job_id = row[0]
                    job_url = row[1]
                    job_title = row[2]
                    company_name = row[3]
                    job_location = row[4]
                    posted_date = row[5]
                    job_link_id = row[6] if row[6] else None
                    job_description = row[7] if row[7] else None
                    application_type = row[9] if row[9] else "offSite"
                    company_email = eval(row[10]) if row[10] else None
                    job_official_url = row[11] if row[11] else None
                    job = Job(job_id, job_url, job_title, company_name, job_location, posted_date, job_link_id, job_description, applied, application_type, company_email, job_official_url)
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
                    row['applied'] = True

        with open(self.csv_file, mode='w',newline='',  encoding='utf-8' ) as file:
            flocker.lockForWrite(file)
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(job_data)
            flocker.unlock(file)
    