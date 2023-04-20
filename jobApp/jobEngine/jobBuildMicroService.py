from jobBuilderLinkedin import JobBuilder

# TODO Move all paths required for a service  to a config file

class JobBuilderMicroService:
    def __init__(self,service_name="job builder", csv_links="jobApp/data/links.csv", csv_jobs="jobApp/data/jobs.csv"):
        self.name = service_name
        print(f"initialising {self.name} microservice..")        
        self.jobber = JobBuilder(None, "offSite", csv_links, csv_jobs ) 

    def run_service(self):
        print(f"running {self.name} microservice..")
        self.jobber.createJobObjectList()
        #self.jobber.storeAsCsv('jobApp/data/jobs.csv')


if __name__ == '__main__':
    import sys
    args = sys.argv
    csv_links = ""
    csv_jobs = ""
    # get the csv links
    if args[1] and args[2]:
        csv_links=args[1]
        csv_jobs= args[2]
        print(f"csv links file: {csv_links}")
        print(f"csv jobs file: {csv_jobs}")
        jlink = JobBuilderMicroService(csv_file=csv_links, csv_jobs=csv_jobs)
        jlink.run_service()
    else:
        jlink = JobBuilderMicroService()
        jlink.run_service()