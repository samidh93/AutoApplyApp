from .jobEngine.linkedin.jobScraperLinkedin import JobScraperLinkedin
import logging
logger = logging.getLogger(__name__)

""" collect jobs from linkedin and save them localy"""

class JobScraperLinkedinMicroService:
    def __init__(self,service_name="job scraper linkedin",linkedin_data='jobApp/secrets/linkedin.json',  csv_file_out='jobApp/data/jobs.csv', num_pages_to_visit = 5):
        self.name = service_name
        logger.info(f"initialising {self.name} microservice..")        
        self.jobParserObj= JobScraperLinkedin(linkedin_data, csv_file_out ,"internal")
        self.num_pages = num_pages_to_visit

    def run_service(self):
        logger.info(f"running {self.name} microservice..")
        self.jobParserObj.searchJobsThreads(self.num_pages) # run collector and return list of jobs
        self.jobsCountFound = self.jobParserObj.total_jobs
        self.jobsLinks = self.jobParserObj.job_details_list
        return self.jobsCountFound, self.jobsLinks

    def get_jobs_found(self):
        logger.info(f"running {self.name} microservice..")
        self.jobsCountFound = self.jobParserObj.getJobCountFound()
        self.jobParserObj.driver.quit()
        return self.jobsCountFound

#if __name__ == '__main__':
#    jlink = JobScraperLinkedinMicroService()
#    jlink.run_service()