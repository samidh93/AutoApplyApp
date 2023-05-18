from applicationDirector import ApplicationDirector
from candidateProfile import CandidateProfile

# TODO Move all paths required for a service  to a config file
    
class easyApplyMicroService:

    def __init__(self, service_name="easy apply", csv_jobs='jobApp/data/jobs.csv'):
        self.name = service_name
        print(f"initialising {self.name} microservice..")
        candidate = CandidateProfile(resume_path='jobApp/data/zayneb_dhieb_resume_english.pdf', 
                                     firstname="zayneb", lastname="dhieb", 
                                     email= "zaynebdhiab89@gmail.com",   #"dhiebzayneb89@gmail.com", 
                                     phone_number="+21620094923")
        appDirector = ApplicationDirector()
        self.easyapp= appDirector.construct_application(candidate_profile=candidate, jobs=csv_jobs, application_type='Easy Apply')

    def run_service(self):
        print(f"running {self.name} microservice..")
        self.easyapp.ApplyForAll()

if __name__ == '__main__':

    service = easyApplyMicroService()
    service.run_service()