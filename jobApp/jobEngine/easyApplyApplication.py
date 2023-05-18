from applicationAbstract import Application
from jobBuilderLinkedin import JobBuilder, JobParser, Job
from candidateProfile import CandidateProfile, ChatGPT, Resume
from processHandler import ProcessHandler
from linkedinEasyApplyForm import LinkedInEasyApplyForm, WebScraper
import asyncio
import json
import os
from deprecated import deprecated
import csv
import threading

class EasyApplyApplication(Application):
    def __init__(self, candidate_profile: CandidateProfile, jobs: list[Job], csvJobsFile='jobApp/data/jobs.csv'):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Easy Apply'
        super().__init__(candidate=candidate_profile, jobOffers=jobs ,csvJobsFile=csvJobsFile)
        self.pid_login = None
        self.login_task_finished = threading.Event()
        self.login_task_killed = threading.Event()
        # run the login task
        self.runLoginTask()
        # Start the session pairing task -> after login session success 
        self.login_task_finished.wait()
        # create the instance, pass the session 
        self.easyApplyFormObj = LinkedInEasyApplyForm() # the actual logic behind form

    def runLoginTask(self):
        self.loginbot = WebScraper('jobApp/secrets/linkedin.json', headless=False)
        # Start task A
        thread_login = threading.Thread(target=self.loginbot.createLoginSession, args=(self.login_task_finished,self.login_task_killed))
        thread_login.start()
    
    def runLoginProcess(self):
        # process handler
        self.procHandle = ProcessHandler("C:/Users/user1/dev/soft_linkedin_easyAutoApply_Api/jobApp/jobEngine/linkedinLoginSession.py")
        # start login session 
        self.pid_login = self.procHandle.start_process() # start a login session process
        # wait for login session to finish

    def __del__(self):
        if self.pid_login != None:
            print(f"killing process with pid {self.pid_login} after job application is done")
            self.procHandle.kill_last_process()
        else:
            print("terminating login thread ")
            self.login_task_killed.set()
        
    def ApplyForJob(self, job:Job):
        status = False
        print(f"sending easy application for {job.job_title} at {job.company_name} in {job.job_location}")
        status = self.easyApplyFormObj.applyForJob(job.job_url)
        if status:
            job.setJobApplied(True) # applied for job
            print(f"set job applied {job.applied}")
        else:
            job.setJobApplied(False) # not applied for job
            print(f"set job applied {job.applied}")      

    def ApplyForAll(self):
        return super().ApplyForAll("internal")

if __name__ == '__main__':
    candidate = CandidateProfile(resume_path='jobApp/data/zayneb_dhieb_resume_english.pdf', 
                                     firstname="zayneb", lastname="dhieb", 
                                     email= "zaynebdhiab89@gmail.com",   #"dhiebzayneb89@gmail.com", 
                                     phone_number="+21620094923")