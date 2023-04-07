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

import asyncio
from pyppeteer import launch


load_dotenv(find_dotenv())


class JobBuilder:
    def __init__(self, links: list):
        self.links = links
        self.jobObjLists = []

    def createJobObjectList(self) -> list[Job]:

        for i, link in enumerate(self.links):
            response = requests.get(self.links[i])
            if response.status_code == 200:
                # Create an HTML tree from the response text
                tree = html.fromstring(response.text)
                job_id = i + 1  # add an ID to the job
                j = Job(job_id, link, self.getJobTitlefromHtml(tree), self.getCompanyNamefromHtml(tree), self.getLocationfromHtml(
                    tree), self.getPostedDatefromHtml(tree), self.getJobDescriptionFromHtml(tree))
                print(f"Job id: {j.job_id}")
                print(f"Job URL: {j.job_url}")
                print(f"Company Name: {j.company_name}")
                print(f"Job Title: {j.job_title}")
                print(f"Job Location: {j.job_location}")
                print(f"Posted Date: {j.posted_date}")
                print(f"Job Description: {j.job_description[0:100]}")
                print("\n")
                self.jobObjLists.append(j)

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
            desc = source_html.xpath('//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div')[0]
            text = desc.text_content()
        except IndexError:
            print("Index out of range: No posted date found")
            text = "na"

        return text


if __name__ == '__main__':
    # TODO: add json parser
    jobParserObj = JobParser(job_title="recruiting", location="France")
    jobs = jobParserObj.generateLinksPerPage(1)
    jobber = JobBuilder(jobs)
    jobber.createJobObjectList()
