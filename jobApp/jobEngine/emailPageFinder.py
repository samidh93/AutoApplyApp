"""
a class that tries to extract/find email from given url
"""
import requests
import re
import time
class EmailExtractor:
    def __init__(self, url) -> list:
         self.url = url
    
    # Define a function to retrieve the HTML content of a given URL
    def _get_html(self,url):
        max_retry = 5
        for _ in range(max_retry):
            response = requests.get(url)
            if response.status_code == 200:
                return response.content.decode('utf-8')
            else:
                print(
                    f"error response from link {response.status_code} , retry")
                time.sleep(5)  # we slow down requests for 5 seconds
                continue  # we continue with next retry

        
    # Define a function to search for email addresses within the HTML
    def _find_emails(self,html)->list:
        # Define a regular expression pattern to match email addresses
        pattern = r'\b(?!.*\bsvg\b)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # Search for the pattern within the HTML using the re module
        matches = re.findall(pattern, html)
        # Return a list of unique email addresses
        return list(set(matches))
    
    def extract_emails(self):
        return self._find_emails(self._get_html(self.url))

if __name__ == '__main__':
    url = "https://www.linkedin.com/jobs/view/human-resources-business-partner-m-w-d-at-precise-hotels-and-resorts-3501261094/?trackingId=%2Fuwj9NQZdAugrPlW7nV3BQ%3D%3D&refId=dSj9QT7BKc5IgT0DLp5LJg%3D%3D&pageNum=0&position=20&trk=public_jobs_jserp-result_search-card&originalSubdomain=de"
    print(EmailExtractor(url).extract_emails())