from ..application.applicationAbstract import Application, print_progress_bar
from ..job.job import Job
from ..user.candidateProfile import CandidateProfile
from ..utils.processHandler import ProcessHandler
from ..linkedin.linkedinEasyApplyForm import LinkedInEasyApplyFormHandler
from ..linkedin.loginSessionLinkedin import LoginSessionLinkedCreator
from deprecated import deprecated
import threading
from selenium import webdriver
import time
from ..linkedin.linkedinSeleniumBase import LinkedinSeleniumBase
import logging
logger = logging.getLogger(__name__)

class EasyApplyApplication(Application):
    def __init__(self, candidate_profile: CandidateProfile,  csvJobsFile='jobApp/data/jobs.csv', linkedinData=None):
        super().__init__(candidate=candidate_profile, csvJobsFile=csvJobsFile, linkedin_data=linkedinData)
        self.candidate_profile = candidate_profile
        self.type = 'Easy Apply'
        self.pid_login = None
        self.login_task_finished = threading.Event()
        self.login_task_killed = threading.Event()
        # create the instance, pass the session: pass down the candidate profile object
        self.easyApplyFormObj = LinkedInEasyApplyFormHandler(candidate_profile=candidate_profile, csv_jobs=csvJobsFile , linkedin_data_file=linkedinData) # the actual logic behind form

    def runLoginTask(self):
        self.loginbot = LoginSessionLinkedCreator('jobApp/secrets/linkedin.json', headless=False)
        # Start task A
        thread_login = threading.Thread(target=self.loginbot.createLoginSession, args=(self.login_task_finished,self.login_task_killed))
        thread_login.start()
    
    def runLoginProcess(self):
        # process handler
        self.procHandle = ProcessHandler("C:/Users/user1/dev/soft_linkedin_easyAutoApply_Api/jobApp/jobEngine/linkedinLoginSession.py")
        # start login session 
        self.pid_login = self.procHandle.start_process() or None# start a login session process
        # wait for login session to finish

    def __del__(self):
        pass
        if self.pid_login != None:
            logger.info(f"killing process with pid {self.pid_login} after job application is done")
            self.procHandle.kill_last_process()
        else:
            logger.info("terminating login thread ")
            self.login_task_killed.set()
        
    def ApplyForJob(self, job:Job, cookies:list ):
        applied = False
        driver = LinkedinSeleniumBase(self.linkedin_data).driver
        logger.info(f"sending easy application for {job.job_title} at {job.company_name} in {job.job_location}")
        try:
            applied = self.easyApplyFormObj.applyForJob(job.link,driver, cookies, True, 900)
            if applied:
                job.setJobApplied(True) # applied for job
                logger.info(f"is job success applied: {job.applied}")
                self.update_job_status(job=job)
                # Update the progress bar dynamically
                with self.lock:
                    self.completed_jobs += 1
                    print_progress_bar(self.completed_jobs, len(self.jobs))
                    if self.completed_jobs >= self.application_limit:
                        logger.info("application limit, requesting shutdown..")
                        self.limit_reached_event.set()
            else:
                job.setJobApplied(False) # not applied for job
                logger.info(f"is job success applied: {job.applied}")    
            
        except Exception as E:
            logger.error(f"error {E} applying to job: {job.job_id}")
        finally:
            driver.quit()

    def ApplyForAll(self):
        return super().ApplyForAll("internal", application_limit=self.candidate_profile.applications_limit)
    
    def getAppliedJobs(self):
        return super().get_applied_jobs()

if __name__ == '__main__':
    candidate = CandidateProfile(resume_path='jobApp/data/resume.pdf', 
                                     firstname="first", lastname="last", 
                                     email= "use@gmail.com",   #"email@gmail.com", 
                                     phone_number="+phone")