import requests
from bs4 import BeautifulSoup
from seleniumWrapper import WebScraper
class JobParser:
    def __init__(self, base_url='https://www.linkedin.com/jobs/search/', job_title=str, location=str, page_num=1):
        self.base_url = base_url 
        self.page_num = page_num
        self.job_title= job_title
        self.location = location
        self.page_num = page_num
        self.job_pos = 1
        self.filter_easy_apply = False
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'position': self.job_pos, # 25 per page
            'pageNum': self.page_num # we increment this for next page
        }
        self.jobList = []

    def setEasyApplyFilter(self, easy_apply_filter):
        print("Warning: This statement has not effect if no user is logged in !\n \
               easy apply filter is only visible for logged user:\n \
              use linkedin api or selenium to scrape links as authenticated user  ")
        self.filter_easy_apply = easy_apply_filter
        if easy_apply_filter:
            self.params['f_AL']=easy_apply_filter
        if not easy_apply_filter:
            if 'f_AL' in self.params:
                self.params.pop('f_AL')
                self.filter_easy_apply = False

    def generateLinks(self):
        if self.filter_easy_apply:
            return self._use_selenium_to_get_easy_apply_jobs()
        response = requests.get(self.base_url, params=self.params)
        html_source = response.content
        # Create a BeautifulSoup object to parse the HTML source code
        soup = BeautifulSoup(html_source, "html.parser")
        # Find the element
        no_jobs = soup.find(class_="results-context-header__job-count")
        # Check if the element was found
        if no_jobs:
            # Print the contents of the no_jobs
            print("total job found: "+str(no_jobs.contents))
        else:
            print("no_jobs not found")
        # Find the element with the id 'results-list__title'
        element = soup.select_one('#main-content > section.two-pane-serp-page__results-list > ul')
        # Find all <li> elements
        li_elements = element.find_all('li')
        links = []
        for li in li_elements:
            if li.find("a") and "href" in li.a.attrs:
                href = li.a["href"]
                #print("link to job: "+str(href)+ "\n")
                links.append(href)
        print(len(links))
        self.jobList+= links
        return self.jobList
    
    def generateLinksPerPage(self, max_pages = 5)-> list: #125 jobs
        for _ in range(max_pages):
            self.generateLinks()
        return self.jobList
    
    def _use_selenium_to_get_easy_apply_jobs(self):
        scraper = WebScraper(headless=True)
        scraper.login_user()
        return scraper.getEasyApplyJobLinks(self.base_url, self.params)

if __name__ == '__main__':
   # TODO: add json parser
   jobParserObj= JobParser(job_title="recruiting", location="France")
   jobParserObj.setEasyApplyFilter(True)
   jobs = jobParserObj.generateLinksPerPage(1)
   print(jobs)
   print(len(jobs))

