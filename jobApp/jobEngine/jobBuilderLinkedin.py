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
from abc import ABC, abstractmethod
import csv
from emailCompanyBuilder import EmailCompanyBuilder
from fileLocker import FileLocker
"""jbo builder class to create job object list

    Returns:
        list[job]: see class Job
    """

load_dotenv(find_dotenv())


class JobBuilder:

    # TODO Add new classes: EasyApplyJobBuilder, OffsiteJobBuilder
    def __init__(self, links: list, application_type: str, csv_links='jobApp/data/links.csv'):
        self.links = links
        self.jobObjLists = []
        self.application_type = application_type
        self.requests_counter = 0
        self.csv_file = csv_links
        if csv_links:
            print("loading links from file directly")
            self.load_links_from_csv()

    def load_links_from_csv(self):
        links = [[], [], []]  # list of 2 lists
        flocker =FileLocker()
        if os.path.isfile(self.csv_file):
            # Read
            with open(self.csv_file, mode='r', newline='') as file:
                flocker.lockForRead(file)
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for i, row in enumerate(reader):
                    links[0].append(row[4])  # intern links
                    links[1].append(row[5])  # extern links
                    links[2].append(row[3])  # link_id
                flocker.unlock(file)

        self.links = links

    def createJobObjectList(self) -> list[Job]:
        max_retry = 5
        start_time = time.time()
        for i, link in enumerate(self.links[0]):
            self.requests_counter += 1
            # we try 5 times if server retrun code 429 (too many requests in period of time)
            for _ in range(max_retry):
                try:
                    response = requests.get(link)
                    if response.status_code == 200:
                        # Create an HTML tree from the response text
                        tree = html.fromstring(response.text)
                        job_id = i + 1  # add an ID to the job
                        job_title = self.getJobTitlefromHtml(tree)
                        company_name = self.getCompanyNamefromHtml(tree)
                        location = self.getLocationfromHtml(tree)
                        posted_date = self.getPostedDatefromHtml(tree)
                        job_description = self.getJobDescriptionFromHtml(tree)
                        intern_link = link
                        extern_link = self.links[1][i]
                        link_id = self.links[2][i]
                        emails = EmailCompanyBuilder.getJobEmails(
                            company_name, location, response.content.decode('utf-8'),  intern_link, extern_link)
                        j = Job(job_id, intern_link, job_title, company_name, location, posted_date, link_id,
                                job_description, False, company_email=emails, job_official_url=extern_link)
                        print(f"Job id: {j.job_id}")
                        print(f"Job link_id: {j.job_link_id}")
                        print(f"Job URL: {j.job_url}")
                        print(f"Company Name: {j.company_name}")
                        print(f"Company Emails: {j.company_email}")
                        print(f"Job Title: {j.job_title}")
                        print(f"Job Location: {j.job_location}")
                        print(f"Posted Date: {j.posted_date}")
                        print(f"Job Description: {j.job_description[0:100]}")
                        print(f"Applied: {j.applied}")
                        print(f"application type: {j.application_type}")
                        print(f"job official url: {j.job_official_url}")
                        print("\n")
                        self.jobObjLists.append(j)
                        break  # no need for retry
                    elif response.status_code == 429:
                        end_time = time.time()
                        print(
                            f"error {response.status_code}: too  many requests. number of requests per seconds: \n \
                             {self.requests_counter}/{end_time-start_time}  slowing down requests time to 5 sec ")
                        time.sleep(5)  # we slow down requests for 5 seconds
                        continue  # we continue with next retry

                except requests.exceptions.Timeout as err:
                    print(f"Request timed out: {err}")
                    time.sleep(3)  # we slow down requests for 5 seconds
                    continue

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
        fieldnames = ["job_id",  "job_url","job_title", "company_name", 
            "job_location", "posted_date","job_link_id", "job_description", 
            "applied", "application_type", "company_emails", "official_job_url"]
        flocker = FileLocker()
        # write the data to the CSV file
        with open(file_name, mode="w", newline='') as csv_file:
            # we lock for writing
            flocker.lockForWrite(csv_file)
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)
            for job in self.jobObjLists:
                writer.writerow([
                    job.job_id,
                    job.job_url,
                    job.job_title,
                    job.company_name,
                    job.job_location,
                    job.posted_date,
                    job.job_link_id,
                    job.job_description,
                    job.applied,
                    job.application_type,
                    job.company_email,
                    job.job_official_url
                ])
            flocker.unlock(csv_file)
        print(f"{len(self.jobObjLists)} job(s) stored in {file_name}.")
        


if __name__ == '__main__':

    jobber = JobBuilder(None, "offSite", "jobApp/data/links.csv" ) 
    jobber.createJobObjectList()
    jobber.storeAsCsv('jobApp/data/jobs.csv')
