import requests
from bs4 import BeautifulSoup, Comment
from seleniumWrapper import WebScraper
import json
import csv
import os
import re
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin

class JobParser:
    def __init__(self, linkedin_data):
        """Parameter initialization"""
        with open(linkedin_data) as config_file:
            data = json.load(config_file)
        self.base_url = data["urls"]['search_job_url']
        self.page_num = data["params"]['pageNum']
        self.job_title= data["login"]['keywords']
        self.location = data["login"]['location']
        self.job_pos = data["params"]['start']
        self.filter_easy_apply = data["params"]['f_AL']
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'position': self.job_pos, # 25 per page
            'pageNum': self.page_num, # we increment this for next page
            'f_AL': self.filter_easy_apply # we increment this for next page
        }
        self.jobList = []
        self.easyApplyList = []
        self.offsiteApplyList = []
        self.officialJobLinks = []
        # the bot
        self.bot = EasyApplyLinkedin('jobApp/secrets/linkedin.json', headless=True)


    def setEasyApplyFilter(self, easy_apply_filter=False):
        print("Warning: easy apply filter is only visible for logged user ")
        self.filter_easy_apply = easy_apply_filter
        # set the filter to true or false
        self.params['f_AL']=easy_apply_filter

    def generateLinksPerPage(self, max_pages = 5)-> list: #125 jobs
        for _ in range(max_pages):
            self.generateLinks()
        #@NOTE: added save to csv to keep track of links
        if self.filter_easy_apply:
            self.saveLinksToCsv(links= [self.easyApplyList, "na"])
            return [self.easyApplyList, "na"]
        else:
            self.saveLinksToCsv(links= [self.offsiteApplyList, self.officialJobLinks ])
            return [self.offsiteApplyList, self.officialJobLinks ]
        
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
        element = soup.select_one('#main-content > section.two-pane-serp-page__results-list > ul')
        # Find all <li> elements
        li_elements = element.find_all('li')
        links = []
        for li in li_elements:
            if li.find("a") and "href" in li.a.attrs:
                href = li.a["href"]
                print("link to job found: "+str(href))
                if self.filter_easy_apply: # if we are looking only for easy apply jobs
                    self.filterJobList(href, True, False)
                    links.append(href)  # keep track of global links
                else:
                    self.filterJobList(href, False, True)
                    links.append(href)              
        self.jobList+= links
        print(f"total links found {len(self.jobList)}")
        if self.filter_easy_apply:
            print(f"total links easy apply found {len(self.easyApplyList)}")  
            return  [self.easyApplyList, "na"]
        else:
            print(f"total links offsite apply found {len(self.offsiteApplyList)}") 
            return [self.offsiteApplyList, self.officialJobLinks ]
        
    def generateLinksSeleniumV2(self, pages=5):
        self.bot.getEasyApplyJobSearchUrlResults()
        self.jobList = self.bot.getUnlockJobLinksNoLogin(pages) # we have all links
        for link in self.jobList:
            if self.filter_easy_apply: # if we are looking only for easy apply jobs
                self.filterJobList(link, True, False)
            else:
                self.filterJobList(link, False, True)
        if self.filter_easy_apply:
            print(f"total links easy apply found {len(self.easyApplyList)}")  
            self.saveLinksToCsv(links= [self.easyApplyList, "na"])
            return  [self.easyApplyList, "na"]
        else:
            print(f"total links offsite apply found {len(self.offsiteApplyList)}") 
            self.saveLinksToCsv(links= [self.offsiteApplyList, self.officialJobLinks ])
            return [self.offsiteApplyList, self.officialJobLinks ]

    def filterJobList(self, job_href, onsite=False, offsite=False )-> list:
            response = requests.get(job_href)
            html_source = response.content
            # Create a BeautifulSoup object to parse the HTML source code
            soup = BeautifulSoup(html_source, "html.parser")
            if offsite:
                button = soup.find('button', {'data-tracking-control-name': 'public_jobs_apply-link-offsite_sign-up-modal'})
                if button is not None:
                    print("offsite apply ")
                    self.offsiteApplyList.append(job_href)
                    self.getOfficialJobLink(soupObjRef=soup)
                    return self.offsiteApplyList
                else:
                    print("button offsite not found \n")  

            if onsite:
                button = soup.find('button', {'data-tracking-control-name': 'public_jobs_apply-link-onsite'})
                if button is not None:
                    print("onsite apply \n")
                    self.easyApplyList.append(job_href)
                    return self.easyApplyList
                else:
                    print("button onsite not found \n")  

    def getOfficialJobLink(self, soupObjRef:BeautifulSoup):
        #soup = BeautifulSoup(html_doc, "html.parser")
        # find the element with the 'id' attribute value of 'applyUrl'
        apply_url_element = soupObjRef.find(id='applyUrl')
        # find the comment node inside the 'applyUrl' element
        comment_node = (apply_url_element.find(string=lambda string: isinstance(string, Comment)))
        official_link = comment_node.replace('"', '')
        # print the text content of the comment node
        print(f"official job link: {official_link}\n")
        self.officialJobLinks.append(official_link)
         
    def extract_link_id(self, link:str):
        # find the first occurrence of "?"
        question_mark_index = link.find("?")
        # extract the substring before "?"
        id_string = link[:question_mark_index]
        # find the last occurrence of "-" before "?"
        dash_index = id_string.rfind("-")
        # extract the substring after the last "-"
        id = id_string[dash_index+1:]
        return id

    def saveLinksToCsv(self, links, csv_file='jobApp/data/links.csv'):
        # Check if the CSV file exists: read and append only new links
        ids = list()
        counter = 0
        if os.path.isfile(csv_file):
            # Read
            with open(csv_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    ids.append(row[3]) # we get all ids there
            # write
            
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                for i, link in enumerate(links[0]): # new links loop
                    if self.extract_link_id(link) not in ids: 
                        counter +=1
                        writer.writerow([len(ids)+counter, self.job_title, self.location, self.extract_link_id(link) , link, links[1][i]])
        # no csv, write new from zero
        else: 
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header row if the file is empty
                if os.stat(csv_file).st_size == 0:
                    writer.writerow(['id', 'keyword', 'location','link id', 'internal link', 'external link'])
                for i, link in enumerate(links[0]):
                    writer.writerow([i+1, self.job_title, self.location, self.extract_link_id(link) , link, links[1][i]])
        print(f"Links saved to {csv_file}")


if __name__ == '__main__':

   jobParserObj= JobParser('jobApp/secrets/linkedin.json')
   jobParserObj.setEasyApplyFilter(False)
   jobsLinks = jobParserObj.generateLinksSeleniumV2()
