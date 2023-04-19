from emailPageFinder import EmailExtractor
from emailRandomGenerator import emailCompanyGenerator 
from job import Job

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
            print("-------------------------------------------------------------------------")
            try:
                print("try finding emails from the job url by portal link")
                extracted = EmailExtractor(job.job_url).extract_emails()
                if len(extracted)>0:
                    job.setCompanyEmail(extracted)
                    self.emails.extend(extracted)
                    print(f"company {job.company_name} email {extracted} found")
                    continue
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
                if len(extracted)>0:
                    job.setCompanyEmail(extracted)
                    self.emails.extend(extracted)
                    print(f"company {job.company_name} email {extracted} found")
                    continue
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
                if len(generated)>0:
                    job.setCompanyEmail(generated)
                    self.emails.extend(generated)
                    print(f"company {job.company_name} in {job.job_location} emails {generated} generated")
                else:
                    raise ValueError("The emails list is empty")
            except ValueError as e:
                print(e)  
                print("generation with ai failed, aborting job..")
            print("-------------------------------------------------------------------------")
    
    @staticmethod
    def getJobEmails( company_name, company_location, html, intern_link, extern_link):
            print("-------------------------------------------------------------------------")
            try:
                print("try finding emails from the job url by portal link")
                extracted = EmailExtractor(intern_link).extract_emails(html)
                if len(extracted)>0:
                    print(f"company {company_name} email {extracted} found")
                    return extracted
                else:
                    raise ValueError("The emails list is empty")
            except ValueError as e:
                print(e)  
                print("extraction from job link failed, try next method..")
            ####################################
            ####################################
            try:
                print("try finding emails from the job url by official link")
                extracted = EmailExtractor(extern_link).extract_emails(html)
                if len(extracted)>0:
                    print(f"company {company_name} email {extracted} found")
                    return extracted
                else:
                    raise ValueError("The emails list is empty")
            except ValueError as e:
                print(e)  
                print("extraction from job link failed, try next method..")
            ####################################################
            ####################################################
            try:
                print("try generating emails with AI")
                generated = emailCompanyGenerator(company_name, company_location).generate_emails()
                if len(generated)>0:
                    print(f"company {company_name} in {company_location} emails {generated} generated")
                    return generated
                else:
                    raise ValueError("The emails list is empty")
            except ValueError as e:
                print(e)  
                print("generation with ai failed, aborting job..")
            print("-------------------------------------------------------------------------")   

if __name__ == '__main__':
    pass
    


