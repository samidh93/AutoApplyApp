import requests
from bs4 import BeautifulSoup, Comment
from seleniumWrapper import WebScraper
import json
import csv
import os
import re
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin
from fileLocker import FileLocker
import time


class JobParser:
    def __init__(self, linkedin_data, csv_links='jobApp/data/links.csv'):
        """Parameter initialization"""
        with open(linkedin_data) as config_file:
            data = json.load(config_file)
        self.base_url = data["urls"]['search_job_url']
        self.page_num = data["params"]['pageNum']
        self.job_title = data["login"]['keywords']
        self.location = data["login"]['location']
        self.job_pos = data["params"]['start']
        self.filter_easy_apply = data["params"]['f_AL']
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'position': self.job_pos,  # 25 per page
            'pageNum': self.page_num,  # we increment this for next page
            'f_AL': self.filter_easy_apply  # we increment this for next page
        }
        self.jobList = []
        self.easyApplyList = []
        self.offsiteApplyList = []
        self.officialJobLinks = []
        # the bot
        self.bot = EasyApplyLinkedin(
            'jobApp/secrets/linkedin.json', headless=True)
        self.csv_file = csv_links
        # pair to store links {"onsite": None, "offsite": None}
        self.links_pair = {"onsite": "None", "offsite": "None"}
        # list of dict [ {"onsite": None, "offsite": None} ]
        self.links_pair_list = []

    def setEasyApplyFilter(self, easy_apply_filter=False):
        print("Warning: easy apply filter is only visible for logged user ")
        self.filter_easy_apply = easy_apply_filter
        # set the filter to true or false
        self.params['f_AL'] = easy_apply_filter

    def generateLinksPerPage(self, max_pages=5) -> list:  # 125 jobs
        for _ in range(max_pages):
            self.generateLinks()
        # @NOTE: added save to csv to keep track of links
        if self.filter_easy_apply:
            self.saveLinksToCsv(links=[self.easyApplyList, "na"])
            return [self.easyApplyList, "na"]
        else:
            self.saveLinksToCsv(
                links=[self.offsiteApplyList, self.officialJobLinks])
            return [self.offsiteApplyList, self.officialJobLinks]

    def generateLinks(self):
        full_url = f"{self.base_url}?{'&'.join([f'{k}={v}' for k, v in self.params.items()])}"
        print(f"constructed url: {full_url }")
        response = requests.get(self.base_url, params=self.params)
        html_source = response.content
        # Create a BeautifulSoup object to parse the HTML source code
        soup = BeautifulSoup(html_source, "html.parser")
        # Find the element
        jobCount = soup.find(class_="results-context-header__job-count")
        # Check if the element was found
        if jobCount:
            # Print the contents of the jobCount
            print("total job found: "+str(jobCount.contents))
        else:
            print("jobCount not found")
        # Find the element with the id 'results-list__title'
        element = soup.select_one(
            '#main-content > section.two-pane-serp-page__results-list > ul')
        # Find all <li> elements
        li_elements = element.find_all('li')
        links = []
        for li in li_elements:
            if li.find("a") and "href" in li.a.attrs:
                href = li.a["href"]
                print("link to job found: "+str(href))
                if self.filter_easy_apply:  # if we are looking only for easy apply jobs
                    self.filterJobList(href, True, False)
                    links.append(href)  # keep track of global links
                else:
                    self.filterJobList(href, False, True)
                    links.append(href)
        self.jobList += links
        print(f"total links found {len(self.jobList)}")
        if self.filter_easy_apply:
            print(f"total links easy apply found {len(self.easyApplyList)}")
            return [self.easyApplyList, "na"]
        else:
            print(
                f"total links offsite apply found {len(self.offsiteApplyList)}")
            return [self.offsiteApplyList, self.officialJobLinks]

    def generateLinksSeleniumV2(self, pages=5):
        self.bot.getEasyApplyJobSearchUrlResults()
        self.jobList = self.bot.getUnlockJobLinksNoLogin(
            pages)  # we have all links
        for i, link in enumerate(self.jobList):
            print(f"filtering job with index {i}")
            pair = self.filterJobList(link)
            print(f"pair: {pair}")
            self.links_pair_list.append(pair)
        print(f"list: {self.links_pair_list}")
        self.saveLinksToCsv(self.links_pair_list, self.csv_file)

    def filterJobList(self, job_href, onsite=False, offsite=False) -> dict:
        links_pair = {"onsite": "None", "offsite": "None"}
        response = requests.get(job_href)
        html_source = response.content
        # @NOTE: the requests here to be moved while getting the url at the same step
        time.sleep(1)  # slow down request
        # Create a BeautifulSoup object to parse the HTML source code
        soup = BeautifulSoup(html_source, "html.parser")
        # find offsite apply
        button = soup.find('button', {
                           'data-tracking-control-name': 'public_jobs_apply-link-offsite_sign-up-modal'})
        # public_jobs_apply-link-onsite
        if button is not None:  # if found
            print("offsite apply button found")
            # self.offsiteApplyList.append(job_href)
            offsite_link = self.getOfficialJobLink(soupObjRef=soup)
            # {"onsite": None, "offsite": None}
            links_pair["offsite"] = offsite_link
            # {"onsite": None, "offsite": None}
            links_pair["onsite"] = "None"
        else:
            print("button offsite not found, onsite apply is ommited")
            # {"onsite": None, "offsite": None}
            links_pair["offsite"] = "None"
            # {"onsite": None, "offsite": None}
            links_pair["onsite"] = job_href
        return links_pair

    def getOfficialJobLink(self, soupObjRef: BeautifulSoup) -> str:
        # soup = BeautifulSoup(html_doc, "html.parser")
        # find the element with the 'id' attribute value of 'applyUrl'
        apply_url_element = soupObjRef.find(id='applyUrl')
        # find the comment node inside the 'applyUrl' element
        comment_node = (apply_url_element.find(
            string=lambda string: isinstance(string, Comment)))
        official_link = comment_node.replace('"', '')
        # print the text content of the comment node
        print(f"official job link: {official_link}")
        self.officialJobLinks.append(official_link)
        return official_link

    def extract_link_id(self, link: str):
        if link["onsite"] == "None":
            link = link["offsite"]
        else:
            link = link["onsite"]
        # find the first occurrence of "?"
        question_mark_index = link.find("?")
        # extract the substring before "?"
        id_string = link[:question_mark_index]
        # find the last occurrence of "-" before "?"
        dash_index = id_string.rfind("-") 
        if dash_index != -1:# if - found, id write
            id = id_string[dash_index+1:]
        else:
            dash_index = id_string.rfind("/")
            id = id_string[dash_index+1:]        
        return id

    def saveLinksToCsv(self, links, csv_file):
        # Check if the CSV file exists: read and append only new links
        flocker = FileLocker()
        ids = list()
        counter = 0
        if os.path.isfile(csv_file):
            # Read
            with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
                flocker.lockForRead(file)
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    ids.append(row[3])  # we get all ids there
                flocker.unlock(file)
            # write

            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                flocker.lockForWrite(file)
                writer = csv.writer(file)
                for i, link in enumerate(links):  # new links loop
                    if self.extract_link_id(link) not in ids:
                        counter += 1
                        writer.writerow([len(ids)+counter,
                                         self.job_title,
                                         self.location,
                                        self.extract_link_id(link),
                                         link["onsite"],
                                         link["offsite"]])
                flocker.unlock(file)
        # no csv, write new from zero
        else:
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                flocker.lockForWrite(file)
                writer = csv.writer(file)
                # Write the header row if the file is empty
                if os.stat(csv_file).st_size == 0:
                    writer.writerow(
                        ['id', 'keyword', 'location', 'link id', 'internal link', 'external link'])
                for i, link in enumerate(links):
                    writer.writerow([i+1,
                                     self.job_title,
                                     self.location,
                                     self.extract_link_id(link),
                                     link["onsite"],
                                     link["offsite"]])
                flocker.unlock(file)
        print(f"Links saved to {csv_file}")


if __name__ == '__main__':

    jobParserObj = JobParser('jobApp/secrets/linkedin.json')
    jobParserObj.setEasyApplyFilter(False)
    jobsLinks = jobParserObj.generateLinksSeleniumV2()
