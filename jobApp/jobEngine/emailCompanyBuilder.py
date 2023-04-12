from emailPageFinder import EmailExtractor
from emailRandomGenerator import emailCompanyGenerator 
from job import Job
from jobBuilderLinkedin import JobBuilder, JobParser

class EmailCompanyBuilder:
    """ takes a list of jobs, try to find the company emails for each job:
        1- extract email on each link if any
        2- if no email found, try generate random email
        3- if email is not empty, then verify it using gmail 
    """
    def __init__(self, jobs: list[Job]) -> None:
        self.jobs= jobs
        self.emails = []

    def buildEmailList(self) -> list:
        for job in self.jobs:
            try:
                print("try finding emails from the job url by portal link")
                extracted = EmailExtractor(job.job_url).extract_emails()
                if extracted is not []:
                    job.setCompanyEmail(extracted)
                    self.emails.extend(extracted)
                    print(f"company {job.company_name} email {extracted} found")
                    break
                else:
                    raise ValueError("The emails list is empty")
            except ValueError as e:
                print(e)  
                print("extraction from job link failed, try next method..")
            ####################################
            ####################################
            try:
                print("try finding emails from the job url by official link")
                extracted = EmailExtractor(job.job_official_url).extract_emails()
                if extracted is not []:
                    job.setCompanyEmail(extracted)
                    self.emails.extend(extracted)
                    print(f"company {job.company_name} email {extracted} found")
                    break
                else:
                    raise ValueError("The emails list is empty")
            except ValueError as e:
                print(e)  
                print("extraction from job link failed, try next method..")
            ####################################################
            ####################################################
            try:
                print("try generating emails with AI")
                generated = emailCompanyGenerator(job.company_name, job.job_location).generate_emails()
                if generated is not []:
                    job.setCompanyEmail(generated)
                    self.emails.extend(generated)
                    print(f"company {job.company_name} in {job.job_location} emails {generated} generated")
                else:
                    raise ValueError("The emails list is empty")
            except ValueError as e:
                print(e)  
                print("generation with ai failed, aborting job..")

if __name__ == '__main__':
    # TODO: add json parser
    jobParserObj= JobParser('jobApp/secrets/linkedin.json')
    jobParserObj.setEasyApplyFilter(False) # optional as unauthenticated has no access to easy apply 
    jobLinks = jobParserObj.generateLinksPerPage(1)
    jobber = JobBuilder(jobLinks, "offSite" ) # can be upgraeded as a set( links, application_type)
    jobObjList = jobber.createJobObjectList()
    jobber.storeAsCsv('jobApp/data/jobsOffSite.csv')
    emailBuilder = EmailCompanyBuilder(jobObjList)    
    emailBuilder.buildEmailList()


