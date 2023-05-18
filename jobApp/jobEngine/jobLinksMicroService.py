from jobParserLinkedin import JobParser

# TODO Move all paths required for a service  to a config file

class JobLinksMicroService:
    def __init__(self,service_name="job Links", csv_file='jobApp/data/links.csv', num_pages_to_visit = 1):
        self.name = service_name
        print(f"initialising {self.name} microservice..")        
        self.jobParserObj= JobParser('jobApp/secrets/linkedin.json', csv_file )
        self.num_pages = num_pages_to_visit

    def run_service(self):
        print(f"running {self.name} microservice..")
        jobsLinks = self.jobParserObj.generateLinksSeleniumV2(self.num_pages)

if __name__ == '__main__':
    import sys
    args = sys.argv
    csv_links = ""
    # get the csv links
    #if args[1]:
    #    csv_links=args[1]
    #    print(f"csv links file: {csv_links}") 
    #    jlink = JobLinksMicroService(csv_file=csv_links)
    #    jlink.run_service()
    #else:
    jlink = JobLinksMicroService(easyApply=False)
    jlink.run_service()