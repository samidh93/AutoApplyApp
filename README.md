# soft_linkedin_easyAutoApply_Api
web app to automate search and apply for jobs. 

## Description:
This is a web application that uses Selenium, BeautifulSoup4, requests library in Python.
It automates the process of searching job postings on LinkedIn using keywords provided by user
(e.g., "data scientist", etc.)
The script then extracts all relevant information from each posting (job title, company name)
and stores it into an Excel file.
Finally, if desired, users can use this data as input when applying directly through Linkedin's website.

## How To Use It?
this app is based on a microservice architecture. 
The microservices are listed below:
1- job Link microservice: the role of this service is to collect all links based on user search keywords and store then in a database. example storage is under data/links.csv

2- job build microservice: the role of this service is to create  job database links based on the links from the first service. example file is under data/jobs.csv

3- email apply microservice: the role of this service is to send email application to jobs from the jobs database.

4- direct apply microservice: the role of this service is to fill extern form application to jobs from the jobs database.

5- easy apply microservice: the role of this service is to fill easy apply form  application from the jobs database.