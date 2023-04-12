class Job:
    def __init__(self, job_id, job_url,  job_title, company_name, job_location, posted_date, job_description=None, applied=False, application_type="offSite",  company_email=None, job_official_url = None ):

        self.job_id = job_id
        self.job_url = job_url
        self.job_official_url = job_official_url
        self.company_name = company_name
        self.company_email = company_email
        self.job_title = job_title
        self.job_location = job_location
        self.posted_date = posted_date
        self.job_description = job_description
        self.applied = applied
        self.application_type = application_type

    def setCompanyEmail (self, email:list):
        self.company_email = email
    
    def setJobApplied( self, applied):
        self.applied = applied

    def setJobOfficialUrl(self, jobOfficialUrl):
        self.job_official_url = jobOfficialUrl