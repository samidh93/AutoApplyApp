from jobEngine.application.applicationDirector import ApplicationDirector
from jobEngine.user.candidateProfile import CandidateProfile
from jobEngine.config.config import UserConfig, AppConfig

# TODO Move all paths required for a service  to a config file

class easyApplyMicroService:

    def __init__(self, service_name="easy apply", csv_jobs=UserConfig.get_jobs_file_path()):
        self.name = service_name
        print(f"initialising {self.name} microservice..")
        candidate = CandidateProfile(resume_path=UserConfig.get_resume_path("zayneb_dhieb_resume_english.pdf"), 
                                     firstname="Zayneb", lastname="Dhiab", 
                                     email= "dhiebzayneb89@gmail.com",  
                                     phone_number="20094923")
        appDirector = ApplicationDirector()
        self.easyapp= appDirector.construct_application(candidate_profile=candidate, jobs=csv_jobs, application_type='Easy Apply')

    def run_service(self):
        print(f"running {self.name} microservice..")
        self.easyapp.ApplyForAll()

if __name__ == '__main__':

    service = easyApplyMicroService()
    service.run_service()