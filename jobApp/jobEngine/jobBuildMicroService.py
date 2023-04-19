from jobBuilderLinkedin import JobBuilder

# TODO Move all paths required for a service  to a config file

class JobBuilderMicroService:
    def __init__(self,service_name="job builder"):
        self.name = service_name
        print(f"initialising {self.name} microservice..")        
        self.jobber = JobBuilder(None, "offSite", "jobApp/data/links.csv" ) 

    def run_service(self):
        print(f"running {self.name} microservice..")
        self.jobber.createJobObjectList()
        self.jobber.storeAsCsv('jobApp/data/jobs.csv')


if __name__ == '__main__':
    jBuild = JobBuilderMicroService()
    jBuild.run_service()