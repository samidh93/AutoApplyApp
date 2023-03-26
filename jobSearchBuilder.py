import requests
import os, sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class JobBuilder:
    def __init__(self, api_key=None):
        # LinkedIn API credentials
        self.api_key = None or os.getenv("X-RapidAPI-Key")
        self.url = "https://linkedin-jobs-search.p.rapidapi.com/"
        
    def build_jobs(self, search_terms, location, page=1):
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
        }
        payload = {
            "search_terms": search_terms,
            "location": location,
            "page": str(page)
        }
        response = requests.request("POST", self.url, json=payload, headers=headers)
        
        job_objects = []
        if response.status_code == 200:
            jobs_data = response.json()
            for job_data in jobs_data:
                job_url = job_data['job_url']
                linkedin_job_url_cleaned = job_data['linkedin_job_url_cleaned']
                company_name = job_data['company_name']
                company_url = job_data['company_url']
                linkedin_company_url_cleaned = job_data['linkedin_company_url_cleaned']
                job_title = job_data['job_title']
                job_location = job_data['job_location']
                posted_date = job_data['posted_date']
                normalized_company_name = job_data['normalized_company_name']

     

if __name__ == '__main__':
    JobBuilder()
