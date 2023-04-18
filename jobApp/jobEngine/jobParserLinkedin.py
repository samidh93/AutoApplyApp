import requests
from bs4 import BeautifulSoup, Comment
from seleniumWrapper import WebScraper
import json
import csv
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
            return  [self.easyApplyList, "na"]
        else:
            print(f"total links offsite apply found {len(self.offsiteApplyList)}") 
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
    
    def saveLinksToCsv(self, links,  csv_file='jobApp/data/links.csv'):
        # Open the CSV file in write mode
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['id', 'keyword', 'location', 'internal link', 'external link'])
            # Write each row of data to a new row in the CSV file
            for i, link in enumerate(links[0]):
                writer.writerow([i+1, self.job_title, self.location, link, links[1][i] ])
        print(f"links saved to {csv_file}")

    def _use_selenium_to_get_easy_apply_jobs(self):
        scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
        scraper.bot.login_linkedin()
        scraper.bot.getEasyApplyJobSearchUrlResults(jobParserObj.base_url, jobParserObj.params)
        linksToApply = scraper.bot.getJobOffersListEasyApply()

        return linksToApply

if __name__ == '__main__':

   jobParserObj= JobParser('jobApp/secrets/linkedin.json')
   jobParserObj.setEasyApplyFilter(False)
   jobsLinks = jobParserObj.generateLinksPerPage(1)
