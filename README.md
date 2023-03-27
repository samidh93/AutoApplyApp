# soft_linkedin_easyAutoApply_Api
python app to automate searching for jobs, sending emails using AI from famous portal like linkedin.

## Problem to Solve
The goal is to help people automate their job search and application process, eliminating the need to manually search for job postings and complete repetitive tasks for each application.

## Solution Concept Analyzed
To solve this problem, an automated solution will be created that streamlines the job application process for job seekers. The solution will be based on LinkedIn, using LinkedIn APIs to authenticate users, list corresponding job postings, and send job applications.

Note: LinkedIn offers two possibilities for job applications - Easy Apply (directly on LinkedIn by filling out a form) and applying through the company website. To tackle both categories, two solutions are suggested:

Easy Apply: Authentication with a LinkedIn Token will be required. Filling out the form is a straightforward task and can be done using an automated robot (such as Selenium, which has been used in another project).

External Apply: Job data needs to be extracted (e.g., position, country, company, hiring manager, etc.), and then an email will be automatically generated with a cover letter and sent to the hiring manager. A template can be used, or a cover letter can be generated on the fly using AI (an OpenAI Token is needed).

## Technical Solution Proposed
The proposed technical solution involves using LinkedIn's official APIs, including:
https://api.linkedin.com/v2/job-search
https://api.linkedin.com/v2/jobs?_l=en_US
Linkedin has no support for v2 Api for job search yet.

Alternatively, RapidAPI can be used to indirectly access LinkedIn APIs to obtain job search results. However, the free version of RapidAPI has limited requests.

## Job search and sorting 

![jobs searched on linkedin and sorted into job objects to use for next stage](data/jobs.PNG)
