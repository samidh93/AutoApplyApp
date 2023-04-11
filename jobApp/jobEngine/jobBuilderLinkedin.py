import requests
import os
import sys
from dotenv import load_dotenv, find_dotenv
import json
from lxml import html
from job import Job
from bs4 import BeautifulSoup
from jobParserLinkedin import JobParser
from seleniumWrapper import WebScraper
import time


import csv

"""jbo builder class to create job object list

    Returns:
        list[job]: see class Job
    """

load_dotenv(find_dotenv())


class JobBuilder:


    def __init__(self, links: list, application_type: str):
        self.links = links
        self.jobObjLists = []
        self.application_type = application_type

    def createJobObjectList(self) -> list[Job]:
        max_retry = 5
        for i, link in enumerate(self.links):
            # we try 5 times if server retrun code 429 (too many requests in period of time)
            for _ in range(max_retry):
                response = requests.get(self.links[i])
                if response.status_code == 200:
                    # Create an HTML tree from the response text
                    tree = html.fromstring(response.text)
                    job_id = i + 1  # add an ID to the job
                    j = Job(job_id, link, self.getJobTitlefromHtml(tree), self.getCompanyNamefromHtml(tree), self.getLocationfromHtml(
                        tree), self.getPostedDatefromHtml(tree), self.getJobDescriptionFromHtml(tree), False)
                    print(f"Job id: {j.job_id}")
                    print(f"Job URL: {j.job_url}")
                    print(f"Company Name: {j.company_name}")
                    print(f"Job Title: {j.job_title}")
                    print(f"Job Location: {j.job_location}")
                    print(f"Posted Date: {j.posted_date}")
                    print(f"Job Description: {j.job_description[0:100]}")
                    print(f"Applied: {j.applied}")
                    print(f"Job Description: {j.application_type}")
                    print("\n")
                    self.jobObjLists.append(j)
                    break # no need for retry
                else:
                    print(f"error response from link {response.status_code} , retry")
                    time.sleep(5) # we slow down requests for 5 seconds
                    continue # we continue with next retry 

        return self.jobObjLists

    def getJobTitlefromHtml(self, source_html) -> str:
        # Find the element using its class attribute
        try:
            job_title = source_html.xpath(
                '//h1[@class="top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title"]')[0].text.strip()
        except IndexError:
            print("Index out of range: No job title found")
            job_title = "na"

        return job_title

    def getCompanyNamefromHtml(self, source_html) -> str:
        try:
            company_name = source_html.xpath(
                '//a[@class="topcard__org-name-link topcard__flavor--black-link"]')[0].text.strip()
        except IndexError:
            print("Index out of range: No company name found")
            company_name = "na"

        return company_name

    def getLocationfromHtml(self, source_html) -> str:
        try:
            location = source_html.xpath(
                '//span[@class="topcard__flavor topcard__flavor--bullet"]/text()')[0].strip()
        except IndexError:
            print("Index out of range: No location found")
            location = "na"

        return location

    def getPostedDatefromHtml(self, source_html) -> str:
        # Find the element using its class attribute
        try:
            posted_date = source_html.xpath(
                '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[1]/text()')[0].strip()
        except IndexError:
            print("Index out of range: No posted date found")
            posted_date = "na"

        return posted_date

    def getJobDescriptionFromHtml(self, source_html) -> str:

        # Find the element using its class attribute
        try:
            desc = source_html.xpath(
                '//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div')[0]
            text = desc.text_content()
        except IndexError:
            print("Index out of range: No posted date found")
            text = "na"

        return text
    
    def storeAsCsv(self, file_name):
        # define the fieldnames for the CSV file
        fieldnames = ["job_id", "job_url", "company_name", "job_title", "job_location", "posted_date", "job_description", "applied", "application_type"]

        # write the data to the CSV file
        with open(file_name, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for job in self.jobObjLists:
                writer.writerow({
                    "job_id": job.job_id,
                    "job_url": job.job_url,
                    "company_name": job.company_name,
                    "job_title": job.job_title,
                    "job_location": job.job_location,
                    "posted_date": job.posted_date,
                    "job_description": job.job_description,
                    "applied": job.applied, 
                    "application_type": job.application_type
                })
        print(f"{len(self.jobObjLists)} job(s) stored in {file_name}.")
        


if __name__ == '__main__':
    # TODO: add json parser
    jobParserObj= JobParser('jobApp/secrets/linkedin.json')
    jobParserObj.setEasyApplyFilter(False) # optional as unauthenticated has no access to easy apply 
    jobLinks = jobParserObj.generateLinksPerPage(1)
    jobber = JobBuilder(jobLinks, "offSite") # can be upgraeded as a set( links, application_type)
    jobber.createJobObjectList()
    jobber.storeAsCsv('jobApp/data/jobsOffSite.csv')
