"""
a class that tries to extract/find email from given url
"""
import requests
import re

class EmailExtractor:
    def __init__(self, url) -> list:
         self.url = url
    
    # Define a function to retrieve the HTML content of a given URL
    def _get_html(self,url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            raise Exception(f"Failed to retrieve HTML for URL {url}")
            
        
    # Define a function to search for email addresses within the HTML
    def _find_emails(self,html)->list:
        # Define a regular expression pattern to match email addresses
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # Search for the pattern within the HTML using the re module
        matches = re.findall(pattern, html)
        # Return a list of unique email addresses
        return list(set(matches))
    
    def extract_emails(self):
        return self._find_emails(self._get_html(self.url))

if __name__ == '__main__':
    url = "https://carriere.deskeo.fr/jobs/2294634-chef-fe-de-projet-architecture-interieure-cdi?promotion=573308-trackable-share-link-chef-de-projet-architecture-cdi-linkedin"
    print(EmailExtractor(url).extract_emails())