from .jobEngine.application.applicationDirector import ApplicationDirector
from .jobEngine.user.candidateProfile import CandidateProfile
from .jobEngine.config.config import BaseConfig , UserConfig, AppConfig
import json

# TODO Move all paths required for a service  to a config file

class easyApplyMicroService:

    def __init__(self, linkedinConfig, service_name="easy apply", csv_jobs=BaseConfig.get_data_path()):
        self.name = service_name
        print(f"initialising {self.name} microservice..")
        candidate = self.createCandidatePofile(linkedinConfig)
        csv_jobs_file = self.deductUserInCsvJobs(linkedinConfig , csv_jobs)
        appDirector = ApplicationDirector()
        self.easyapp= appDirector.construct_application(candidate_profile=candidate, jobsFile=csv_jobs_file, application_type='Easy Apply')
    
    def run_service(self):
        print(f"running {self.name} microservice..")
        self.easyapp.ApplyForAll()

    ######## utility code: place under another utils module #####
    def createCandidatePofile(self, incomingData):
        json_data = self.loadIncomingDataAsJson(incomingData)
        # User data
        user_data:dict = json_data.get('user')
        email = user_data.get("email")
        self.field_id = user_data.get('field_id')
        # candidate data
        candidate_data:dict = json_data.get("candidate")
        firstname = candidate_data.get('firstname')
        lastname = candidate_data.get('lastname')
        resume = candidate_data.get('resume')
        phone_number = candidate_data.get('phone_number')
        limit = candidate_data.get('limit')
        return CandidateProfile(resume_path=resume, 
                                     firstname=firstname, 
                                     lastname=lastname, 
                                     email=email,  
                                     phone_number=phone_number, 
                                     limit=limit )
    
    def deductUserInCsvJobs(self, incomingData, csv_path:str):
        json_data = self.loadIncomingDataAsJson(incomingData)
        # User data
        job:dict = json_data.get("search_params")
        job_title = job.get('job')
        location = job.get('location')
        return UserConfig.get_jobs_file_path(job_title=job_title, job_location=location,field_id= self.field_id)
        #return self.getUserSearchJobsCsv(csv_path=csv_path, job_title=job_title, job_location=location, field_id=self.field_id)
    
    def replace_spaces_and_commas_with_underscores(self, input_string:str):
        # Replace spaces and commas with underscores
        modified_string = input_string.replace(' ', '_').replace(',', '_')
        return modified_string
    
    def getUserSearchJobsCsv(self, csv_path, job_title, job_location, field_id):
        job_title = self.replace_spaces_and_commas_with_underscores(job_title)
        location = self.replace_spaces_and_commas_with_underscores(job_location)
        csv_extension = ".csv"
        jobs_path = "/jobs"
        file = csv_path+jobs_path+"_"+job_title+"_"+location+"_"+field_id+csv_extension # maybe owner id is needed here
        return file

    def loadIncomingDataAsJson(self, incomingData):
        print("incoming Data: ", incomingData)
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
        return json_data



#if __name__ == '__main__':
#    service = easyApplyMicroService()
#    service.run_service()