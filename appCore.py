#from jobApp.jobScraperLinkedinMicroService import JobScraperLinkedinMicroService
#from jobApp.linkedinEasyApplyMicroService import easyApplyMicroService
from jobApp.loginSessionLinkedinMicroService import  LoginSessionLinkedCreator, LoginException
import logging
logger = logging.getLogger(__name__)

class appCreatorLinkedin:
    def __init__(self, linkedinConfigFile) -> None:
        self.linkedSessionCreatorService = LoginSessionLinkedCreator(linkedinConfigFile)

    def tryCredentialsLinkedin(self):
        try:
            self.linkedSessionCreatorService.attemptLogin()
        except LoginException as E:
            logger.error(f"exception: {E}")
            raise
    def getJobsCount(self):
        try:
            self.linkedSessionCreatorService.attemptLogin()
        except Exception as E:
            logger.error(f"exception: {E}")
            raise    


if __name__ == "__main__":
    
    loginbot = LoginSessionLinkedCreator('jobApp/secrets/linkedin.json')
    bot = loginbot.createLoginSession(True)
