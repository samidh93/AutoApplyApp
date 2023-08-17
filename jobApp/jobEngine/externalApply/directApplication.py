from ..application.applicationAbstract import Application
from ..job.job import  Job
from ..user.candidateProfile import CandidateProfile, ChatGPT, Resume
import json
import os
from deprecated import deprecated
import csv

class DirectApplication(Application):
    def __init__(self, candidate_profile: CandidateProfile, jobs: list[Job], csvJobsFile='jobApp/data/jobs.csv'):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Direct'
        super().__init__(candidate=candidate_profile, jobOffers=jobs ,csvJobsFile=csvJobsFile)

    def ApplyForJob(self, job:Job):
        pass
    
    def ApplyForAll(self):
        return super().ApplyForAll()

if __name__ == '__main__':
    candidate = CandidateProfile(resume_path='jobApp/data/zayneb_dhieb_resume_english.pdf', firstname="zayneb", lastname="dhieb", email="samihomiebro@gmail.com", phone_number="+21620094923")
    jobs = [Job(1, None, "Human Resources Business Partner m/w/d", "precise hotels and resorts","Berlin", "one day ago", "as recruiting specialist you will help us achieve our goals", company_email=["jobs@begu.com"])]
