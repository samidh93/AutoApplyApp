class Job:
    def __init__(self, job_id, job_url,  job_title, company_name, job_location, posted_date, job_description=None, applied=False):

        self.job_id = job_id
        self.job_url = job_url
        self.company_name = company_name
        self.job_title = job_title
        self.job_location = job_location
        self.posted_date = posted_date
        self.job_description = job_description
        self.applied = applied