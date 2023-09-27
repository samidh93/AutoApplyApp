from .jobEngine.application.applicationDirector import ApplicationDirector
from .jobEngine.user.candidateProfile import CandidateProfile
from .jobEngine.config.config import UserConfig, AppConfig
import json

# TODO Move all paths required for a service  to a config file

class easyApplyMicroService:

    def __init__(self, linkedinConfig, service_name="easy apply", csv_jobs=UserConfig.get_data_path()):
        self.name = service_name
        print(f"initialising {self.name} microservice..")
        candidate = self.createCandidatePofile(linkedinConfig)
        csv_jobs_file = self.recreateJobsFile(linkedinConfig , csv_jobs)
        appDirector = ApplicationDirector()
        self.easyapp= appDirector.construct_application(candidate_profile=candidate, jobs=csv_jobs_file, application_type='Easy Apply')
    
    def createCandidatePofile(self, incomingData):
        # load actual user data   
        if isinstance(incomingData, str):
            # If incomingData is a string, assume it's a file path
            try:
                with open(incomingData, 'r') as file:
                    json_data = json.load(file)
            except FileNotFoundError:
                raise FileNotFoundError("File not found")
        elif isinstance(incomingData, dict):
            # If incomingData is a dictionary, assume it's a JSON object
            json_data = incomingData
        else:
            raise ValueError("Invalid incomingData type")
        # User data
        candidate_data:dict = json_data.get("candidate")
        email = candidate_data.get('email')
        firstname = candidate_data.get('firstname')
        lastname = candidate_data.get('lastname')
        resume = candidate_data.get('resume')
        phone_number = candidate_data.get('phone_number')
        limit = candidate_data.get('limit')
        return CandidateProfile(resume_path=resume, 
                                     firstname=firstname, lastname=lastname, 
                                     email= email,  
                                     phone_number=phone_number, limit=limit )
    
    def recreateJobsFile(self, incomingData, csv_path:str):
        # load actual user data   
        if isinstance(incomingData, str):
            # If incomingData is a string, assume it's a file path
            try:
                with open(incomingData, 'r') as file:
                    json_data = json.load(file)
            except FileNotFoundError:
                raise FileNotFoundError("File not found")
        elif isinstance(incomingData, dict):
            # If incomingData is a dictionary, assume it's a JSON object
            json_data = incomingData
        else:
            raise ValueError("Invalid incomingData type")
        # User data
        job:dict = json_data.get("job")
        platform = job.get('platform')
        job_title = job.get('job_title')
        location = job.get('location')
        owner_id = job.get('owner_id')
        created_date = job.get('created_date')
        field_id = job.get('field_id')
        return self.createFileJobLocation(csv_path=csv_path, job_title=job_title, job_location=location, field_id=field_id)
    
    def replace_spaces_and_commas_with_underscores(self, input_string:str):
        # Replace spaces and commas with underscores
        modified_string = ""
        if " " in  input_string:
            modified_string = input_string.replace(' ', '_')
        if "," in input_string:
            modified_string = input_string.replace(',', '_')
        return modified_string
    
    def createFileJobLocation(self, csv_path, job_title, job_location, field_id):
        job_title = self.replace_spaces_and_commas_with_underscores(job_title)
        location = self.replace_spaces_and_commas_with_underscores(job_location)
        csv_extension = ".csv"
        file = csv_path+"_"+job_title+"_"+location+"_"+field_id+"_"+csv_extension # maybe owner id is needed here
        return file


    def run_service(self):
        print(f"running {self.name} microservice..")
        self.easyapp.ApplyForAll()

#if __name__ == '__main__':
#    service = easyApplyMicroService()
#    service.run_service()