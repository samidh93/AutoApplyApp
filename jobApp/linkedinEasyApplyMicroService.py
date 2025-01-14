from .jobEngine.application.applicationDirector import ApplicationDirector
from .jobEngine.application.applicationAbstract import Application
from .jobEngine.user.candidateProfile import CandidateProfile
from .jobEngine.config.config import BaseConfig , UserConfig, AppConfig
import json
import time
import logging
logger = logging.getLogger(__name__)

# TODO Move all paths required for a service  to a config file

class easyApplyMicroService:

    def __init__(self, linkedinConfig, service_name="easy apply", csv_jobs=BaseConfig.get_data_path()):
        self.name = service_name
        logger.info(f"initialising {self.name} microservice..")
        appDirector = ApplicationDirector(linkedinConfig=linkedinConfig, application_type='Easy Apply')
        self.easyapp= appDirector.construct_application(application_type='Easy Apply')
    
    def run_service(self):
        logger.info(f"running {self.name} microservice..")
        self.easyapp.ApplyForAll()
        self.jobsToApply = len(self.easyapp.jobs) # int
        return self.jobsToApply, self.easyapp.jobs
    
    
#if __name__ == '__main__':
#    service = easyApplyMicroService()
#    service.run_service()