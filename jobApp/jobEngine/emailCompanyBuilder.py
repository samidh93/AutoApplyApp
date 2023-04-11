from emailPageFinder import EmailExtractor
from emailRandomGenerator import emailCompanyGenerator 
from job import Job
from jobBuilderLinkedin import JobBuilder

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
            extracted = EmailExtractor(job.job_url).extract_emails()
            if extracted is not []:
                self.emails.extend(extracted)
                print("email extraction success")
            else:
                print("extraction from job link failed: no emails found, try next method..")
                extracted_official = EmailExtractor(job.job_url).extract_emails()
                generated = emailCompanyGenerator("luxoft", "Brussels").generate_emails()


