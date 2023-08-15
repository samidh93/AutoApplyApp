from jobBuilderLinkedin import JobBuilder

# TODO Move all paths required for a service  to a config file


class JobBuilderMicroService:
    def __init__(self, service_name="job builder", csv_links="jobApp/data/links.csv", csv_jobs="jobApp/data/jobs.csv"):
        self.name = service_name
        print(f"initialising {self.name} microservice..")
        self.jobber = JobBuilder(None, csv_links, csv_jobs)

    def run_service(self):
        print(f"running {self.name} microservice..")
        self.jobber.createJobObjectList()
        # self.jobber.storeAsCsv('jobApp/data/jobs.csv')


if __name__ == '__main__':

    jlink = JobBuilderMicroService()
    jlink.run_service()
