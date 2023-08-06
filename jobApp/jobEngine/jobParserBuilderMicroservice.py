from jobParserBuilderCombined import JobParserBuilder

# TODO Move all paths required for a service  to a config file

class JobParserBuilderMicroservice:
    def __init__(self,service_name="job parser builder", config_file='jobApp/secrets/linkedin.json', csv_links_out="jobApp/data/links.csv", csv_jobs_out="jobApp/data/jobs.csv",  num_pages_to_visit = 1):
        self.name = service_name
        print(f"initialising {self.name} microservice..")        
        self.jobCreator= JobParserBuilder(config_file, csv_links_out, csv_jobs_out ,num_pages_to_visit)
        self.num_pages = num_pages_to_visit

    def run_service(self):
        print(f"running {self.name} microservice..")
        jobs = self.jobCreator.generateJobs()

if __name__ == '__main__':

    jobs = JobParserBuilderMicroservice()
    jobs.run_service()