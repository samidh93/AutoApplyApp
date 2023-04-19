from jobParserLinkedin import JobParser

class JobLinksMicroService:
    def __init__(self,service_name="job Links"):
        self.name = service_name
        print(f"initialising {self.name} microservice..")        
        self.jobParserObj= JobParser('jobApp/secrets/linkedin.json')
        self.jobParserObj.setEasyApplyFilter(False)

    def run_service(self):
        print(f"running {self.name} microservice..")
        jobsLinks = self.jobParserObj.generateLinksSeleniumV2()
