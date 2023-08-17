from jobEngine.linkedin.jobScraperLinkedin import JobScraperLinkedin

""" collect jobs from linkedin and save them localy"""

class JobScraperLinkedinMicroService:
    def __init__(self,service_name="job scraper linkedin", csv_file='jobApp/data/jobs.csv', num_pages_to_visit = 5):
        self.name = service_name
        print(f"initialising {self.name} microservice..")        
        self.jobParserObj= JobScraperLinkedin('jobApp/secrets/linkedin.json', csv_file ,"internal")
        self.num_pages = num_pages_to_visit

    def run_service(self):
        print(f"running {self.name} microservice..")
        jobsLinks = self.jobParserObj.createJobsList(self.num_pages)

if __name__ == '__main__':

    jlink = JobScraperLinkedinMicroService()
    jlink.run_service()