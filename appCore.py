from jobApp.jobScraperLinkedinMicroService import JobScraperLinkedinMicroService
from jobApp.linkedinEasyApplyMicroService import easyApplyMicroService
from jobApp.loginSessionLinkedinMicroService import  LoginSessionLinkedCreator, LoginException
import logging
logger = logging.getLogger(__name__)

class appCreatorLinkedin:
    def __init__(self, linkedinConfigFile) -> None:
        #self.linkedSessionCreatorService = LoginSessionLinkedCreator(linkedinConfigFile)
        #self.linkedinJobCollector = JobScraperLinkedinMicroService(linkedin_data=linkedinConfigFile)
        self.linkedinJobApply = easyApplyMicroService(linkedinConfig=linkedinConfigFile)
    
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
    applyReq = {
            "user":{
                "email": "dhiebzayneb89@gmail.com",
                "password": "8862468@",
                "_owner": "_owner",
                "field_id": "id",
                "created_date": "created_date",
            },
            "search_params": {
                "job": "project manager",
                "location": "Germany",
            },
            "candidate":{
                "firstname": "zayneb",
                "lastname": "dhieb", 
                "resume": "https://708f8437-9497-45e7-a86f-8a969c24d91c.usrfiles.com/ugd/4b8c91_0cd5bf0096924bb6990c679beeaa257c.pdf",
                "phone_number": "15731294281",
                "limit": "10",
            }
            # extended with more params such salary and experience
        }
    testapp = appCreatorLinkedin(applyReq)
    testapp.applyJobs()
