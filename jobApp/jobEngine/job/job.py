from urllib.parse import urlparse
import re

class Job:
    def __init__(self, id, job_id, link,  job_title, job_location, company_name, num_applicants, posted_date,
                  job_description=None, company_emails=None, job_poster_name=None,  application_type=None, applied=False):

        #id,job_id,link,title,location,company,number_applicants,date publication
        self.id = id
        self.job_id=job_id
        self.link = link
        self.job_title = job_title
        self.job_location = job_location
        self.company_name = company_name
        self.num_applicants= num_applicants
        self.posted_date = posted_date
        self.job_description = job_description # the text
        self.company_emails = company_emails # list of emails to contact
        self.job_poster_name = job_poster_name # the name of the recruiter
        self.application_type = application_type # internal or external
        self.applied = applied # False 
        self.platform = self.extract_platform(self.link)


    def extract_platform(self, url):
            # Regular expression pattern to match the domain (without top-level domain)
            pattern = r"https?://(?:www\.)?([^/.]+)(?:\.\w+)+"
            # Use re.search to find the domain (without top-level domain) in the URL
            match = re.search(pattern, url)
            if match:
                return match.group(1)
            else:
                return None

    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "link": self.link,
            "job_title": self.job_title,
            "job_location": self.job_location,
            "company_name": self.company_name,
            "num_applicants": self.num_applicants,
            "posted_date": self.posted_date,
            "job_description": self.job_description,
            "company_emails": self.company_emails,
            "job_poster_name": self.job_poster_name,
            "application_type": self.application_type,
            "applied": self.applied
        }

    def setCompanyEmail (self, emails:list):
        self.company_emails = emails
    
    def setJobApplied( self, applied):
        self.applied = applied

