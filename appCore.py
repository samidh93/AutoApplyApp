from jobApp.jobScraperLinkedinMicroService import JobScraperLinkedinMicroService
from jobApp.linkedinEasyApplyMicroService import easyApplyMicroService
from jobApp.loginSessionLinkedinMicroService import  LoginSessionLinkedCreator, LoginException
import logging
logger = logging.getLogger(__name__)

class appCreatorLinkedin:
    def __init__(self, linkedinConfigFile) -> None:
        self.linkedSessionCreatorService = LoginSessionLinkedCreator(linkedinConfigFile)
        self.linkedinJobCollector = JobScraperLinkedinMicroService(linkedin_data=linkedinConfigFile)
        #self.linkedinJobApply = easyApplyMicroService(linkedinConfig=linkedinConfigFile)
    
    def tryCredentialsLinkedin(self):
        try:
            verified = self.linkedSessionCreatorService.attemptLogin()
            return verified
        except LoginException as E:
            logger.error(f"exception: {E}")
            raise 
    def collectJobs(self):
        try:
           jobCount =  self.linkedinJobCollector.run_collect_jobs_service()
           print("number jobs found: ", jobCount)
           return jobCount
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise    
    def applyJobs(self):
        try:
           jobCount =  self.linkedinJobApply.run_service()
           print("number jobs found: ", jobCount)
           return jobCount
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise    


if __name__ == "__main__":
    jobs_query = {
            "search_params": {
                "job": "scrum master",
                "location": "berlin"
            }
        }
    testapp = appCreatorLinkedin(jobs_query)
    jobcount = testapp.getJobsCount()
    print("job count found: ", jobcount)
