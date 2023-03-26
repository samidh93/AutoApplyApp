class Job:
    def __init__(self, job_id, job_url, linkedin_job_url_cleaned, company_name, company_url,
                 linkedin_company_url_cleaned, job_title, job_location, posted_date, normalized_company_name, applied=False):
        print("creating job obj")

        self.job_id = job_id
        self.job_url = job_url
        self.linkedin_job_url_cleaned = linkedin_job_url_cleaned
        self.company_name = company_name
        self.company_url = company_url
        self.linkedin_company_url_cleaned = linkedin_company_url_cleaned
        self.job_title = job_title
        self.job_location = job_location
        self.posted_date = posted_date
        self.normalized_company_name = normalized_company_name
        self.applied = applied