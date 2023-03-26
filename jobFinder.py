import requests
import json
import os, sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# LinkedIn API credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
access_token = os.getenv("ACCESS_TOKEN")

# LinkedIn API endpoints
jobs_search_url = 'https://api.linkedin.com/v2/job-search'
apply_job_url = 'https://api.linkedin.com/v2/normalization/unified-jobs/apply'

# Set headers for API requests
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Set parameters for job search API request
params = {
    'keywords': 'python developer',
    'location': 'United States',
    'company': 'Google',
    'industry': 'Internet'
}

# Send job search API request and get the response
response = requests.get(jobs_search_url, headers=headers, params=params)
response_json = response.json()
print(f"respAPi {response_json}")

# Extract job listings from the API response
job_listings = response_json.get('elements', [])

# Loop through the job listings and apply to each job
for job in job_listings:
    # Set parameters for job application API request
    job_id = job.get('id')
    print(f"job id: {job_id}")
    job_data = {
        'applicant': {
            'email': 'sami.dhiab.x@gmail.com',
            'resume': 'Resume-Sami-Dhiab.pdf',
            'coverLetter': 'cover_sami_dhiab.pdf'
        }
    }

    # Send job application API request and get the response
    apply_response = requests.post(apply_job_url.format(job_id), headers=headers, data=json.dumps(job_data))
    apply_response_json = apply_response.json()
    print(f"respApplyAPi {apply_response_json}")
    # Check if the job application was successful
    if apply_response.status_code == 200 and apply_response_json.get('status') == 'success':
        print(f'Successfully applied to {job.get("title")} at {job.get("companyName")}')
    else:
        print(f'Failed to apply to {job.get("title")} at {job.get("companyName")}')
