from jobApp.jobScraperLinkedinMicroService import JobScraperLinkedinMicroService
from jobApp.linkedinEasyApplyMicroService import easyApplyMicroService
from jobApp.loginSessionLinkedinMicroService import  LoginSessionLinkedCreator, LoginException
import logging
logger = logging.getLogger(__name__)

class appCreatorLinkedin:
    def __init__(self, linkedinConfigFile) -> None:
        self.linkedSessionCreatorService = LoginSessionLinkedCreator(linkedinConfigFile)
        self.linkedinJobCollector = JobScraperLinkedinMicroService(linkedin_data=linkedinConfigFile)

    def tryCredentialsLinkedin(self):
        try:
            self.linkedSessionCreatorService.attemptLogin()
        except LoginException as E:
            logger.error(f"exception: {E}")
            raise
    def getJobsCount(self):
        try:
           jobList, jobCount =  self.linkedinJobCollector.run_service()
           print("number jobs found: ", jobCount)
           return jobList, jobCount
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
    testapp = appCreatorLinkedin(linkedin_data=jobs_query)
    joblist, jobcount = testapp.getJobsCount()
    print("job count found: ", jobcount)
