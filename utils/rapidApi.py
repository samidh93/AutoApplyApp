import requests
import os, sys
from dotenv import load_dotenv, find_dotenv
import json
from job import Job
load_dotenv(find_dotenv())

class JobBuilder:
    def __init__(self, api_key=None):
        # Rapid API credentials
        print("creating job builder obj")
        self.api_key = None or os.getenv("X-RapidAPI-Key")
        self.url_rapidapi = "https://linkedin-jobs-search.p.rapidapi.com/"
        
    def build_jobs(self, search_terms:str, location:str, page=1)-> list:
        headers_rapidapi = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
        }
        payload_rapidApi = {
            "search_terms": search_terms,
            "location": location,
            "page": str(page)
        }

        response = requests.request("POST", self.url_rapidapi, json=payload_rapidApi, headers=headers_rapidapi)
        print(f"server responded: {response}")
        job_objects = []
        if response.status_code == 200:
            print("getting jobs from server ..")
            # Extract the response content in JSON format
            jobs = response.json()
            for i, job in enumerate(jobs):
                job_url = job['job_url']
                linkedin_job_url_cleaned = job['linkedin_job_url_cleaned']
                company_name = job['company_name']
                company_url = job['company_url']
                linkedin_company_url_cleaned = job['linkedin_company_url_cleaned']
                job_title = job['job_title']
                job_location = job['job_location']
                posted_date = job['posted_date']
                normalized_company_name = job['normalized_company_name']
                job_id = i + 1  # add an ID to the job
                j = Job(job_id=job_id, **job)
                print(f"Job id: {j.job_id}")
                print(f"Job URL: {j.job_url}")
                print(f"Cleaned LinkedIn Job URL: {j.linkedin_job_url_cleaned}")
                print(f"Company Name: {j.company_name}")
                print(f"Company URL: {j.company_url}")
                print(f"Cleaned LinkedIn Company URL: {j.linkedin_company_url_cleaned}")
                print(f"Job Title: {j.job_title}")
                print(f"Job Location: {j.job_location}")
                print(f"Posted Date: {j.posted_date}")
                print(f"Normalized Company Name: {j.normalized_company_name}")
                print("\n")
                job_objects.append(j)
        return job_objects
     

if __name__ == '__main__':
   jobObj= JobBuilder()
   jobs = jobObj.build_jobs("ingenieur", "tunisia") # return job object list
   print(jobs)
   
