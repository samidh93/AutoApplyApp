import requests
from bs4 import BeautifulSoup

class FormLocator:
    def __init__(self, url):
        self.url = url
        
    def locate_form(self):
        # Retrieve the HTML content of the URL
        response = requests.get(self.url)
        html = response.text
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the first form element within the HTML
        form = soup.find('form')
        
        if form:
            # Return the form element if found
            print(f"form found within the HTML ")

            return form
        else:
            # Raise an exception if no form element was found
            print("No form element found within the HTML")
        return form

if __name__ == '__main__':
    url = "https://carriere.deskeo.fr/jobs/2294634-chef-fe-de-projet-architecture-interieure-cdi?promotion=573308-trackable-share-link-chef-de-projet-architecture-cdi-linkedin"

    print(FormLocator(url).locate_form())