from .jobEngine.linkedin.jobScraperLinkedin import JobScraperLinkedin

""" collect jobs from linkedin and save them localy"""

class JobScraperLinkedinMicroService:
    def __init__(self,service_name="job scraper linkedin",linkedin_data='jobApp/secrets/linkedin.json',  csv_file_out='jobApp/data/jobs.csv', num_pages_to_visit = 5):
        self.name = service_name
        print(f"initialising {self.name} microservice..")        
        self.jobParserObj= JobScraperLinkedin(linkedin_data, csv_file_out ,"internal")
        self.num_pages = num_pages_to_visit

    def run_service(self):
        print(f"running {self.name} microservice..")
        self.jobsLinks = self.jobParserObj.createJobsList(self.num_pages) # run collector and return list of jobs
        return self.jobsLinks

    def run_job_count_service(self):
        print(f"running job_count microservice..")
        self.jobsCountFound = self.jobParserObj.getJobCountFound() # return the total (optional for testing)
        return self.jobsCountFound

#if __name__ == '__main__':
#    jlink = JobScraperLinkedinMicroService()
#    jlink.run_service()