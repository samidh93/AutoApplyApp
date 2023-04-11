import requests
from bs4 import BeautifulSoup
from seleniumWrapper import WebScraper
import json
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

    def setEasyApplyFilter(self, easy_apply_filter=False):
        print("Warning: easy apply filter is only visible for logged user ")
        self.filter_easy_apply = easy_apply_filter
        # set the filter to true or false
        self.params['f_AL']=easy_apply_filter

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

        print(f"total links found {len(links)}")
        self.jobList+= links
        if self.filter_easy_apply:
            print(f"total links easy apply found {len(self.easyApplyList)}")   
            return  self.easyApplyList
        else:
            print(f"total links offsite apply found {len(self.offsiteApplyList)}") 
            return self.offsiteApplyList
    
    def filterJobList(self, job_href, onsite=False, offsite=False )-> list:
        
            response = requests.get(job_href)
            html_source = response.content
            # Create a BeautifulSoup object to parse the HTML source code
            soup = BeautifulSoup(html_source, "html.parser")
            if offsite:
                button = soup.find('button', {'data-tracking-control-name': 'public_jobs_apply-link-offsite_sign-up-modal'})
                if button is not None:
                    print("offsite apply \n")
                    self.offsiteApplyList.append(job_href)
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
    
    def generateLinksPerPage(self, max_pages = 5)-> list: #125 jobs
        for _ in range(max_pages):
            self.generateLinks()
        if self.filter_easy_apply:
            return self.easyApplyList
        else:
            return self.offsiteApplyList       
    
    def _use_selenium_to_get_easy_apply_jobs(self):
        scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
        scraper.bot.login_linkedin()
        scraper.bot.getEasyApplyJobSearchUrlResults(jobParserObj.base_url, jobParserObj.params)
        linksToApply = scraper.bot.getJobOffersListEasyApply()

        return linksToApply

if __name__ == '__main__':
   from job import Job
   import csv
   from lxml import html
   from job import Job
   from bs4 import BeautifulSoup
   jobParserObj= JobParser('jobApp/secrets/linkedin.json')
   jobParserObj.setEasyApplyFilter(False)
   jobsLinks = jobParserObj.generateLinksPerPage(1)
