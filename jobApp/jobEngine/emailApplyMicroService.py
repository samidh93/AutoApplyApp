from applicationDirector import ApplicationDirector
from candidateProfile import CandidateProfile

    
class EmailApplyMicroService:

    def __init__(self, service_name="email apply"):
        self.name = service_name
        print(f"initialising {self.name} microservice..")
        candidate = CandidateProfile(resume_path='jobApp/data/zayneb_dhieb_resume_english.pdf', firstname="zayneb", lastname="dhieb", email="dhiebzayneb89@gmail.com", phone_number="+21620094923")
        appDirector = ApplicationDirector()
        self.emailapp= appDirector.construct_application(candidate_profile=candidate, jobs='jobApp/data/jobs.csv', application_type='Email')

    def run_service(self):
        print(f"running {self.name} microservice..")
        self.emailapp.ApplyForAll()
    