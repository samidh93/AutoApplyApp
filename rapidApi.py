import requests
from job import Job
from email import GmailSender
from chatgpt import ChatGPT

url = "https://linkedin-jobs-search.p.rapidapi.com/"

payload = {
	"search_terms": "project manager",
	"location": "europe",
	"page": "1"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "ae02d9fe02msh5e0ede937820de2p1f4110jsnfbd13b8aa7c8",
	"X-RapidAPI-Host": "linkedin-jobs-search.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

jobs = [...]  # your list of jobs

job_objects = []
if response.status_code == 200:
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

if __name__ == '__main__':
    chatgpt = ChatGPT(api_key='your_api_key')
    question = "What is the meaning of life?"
    answer = chatgpt.ask(question)
    print(f"Q: {question}\nA: {answer}")
