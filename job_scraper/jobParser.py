import requests
from bs4 import BeautifulSoup

class JobParser:
    def __init__(self, base_url='https://www.linkedin.com/jobs/search/', job_title=str, location=str, page_num=1):
        self.base_url = base_url 
        self.page_num = page_num
        self.job_title= job_title
        self.location = location
        self.page_num = page_num
        self.job_pos = 1
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'position': self.job_pos, # 25 per page
            'pageNum': self.page_num # we increment this for next page
        }
        self.jobList = []
    def generateLinks(self):

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



if __name__ == '__main__':
   # TODO: add json parser
   jobParserObj= JobParser(job_title="recruiting", location="France")
   jobs = jobParserObj.generateLinksPerPage()
   print(jobs)
   print(len(jobs))

