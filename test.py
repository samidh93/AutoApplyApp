import requests
from bs4 import BeautifulSoup
from lxml import html

url = 'https://www.linkedin.com/jobs/search/'
params = {
    'keywords': 'software Engineer',
    'location': 'germany',
    'position': 1, # 25 per page
    'pageNum': 1 # we increment this for next page
}

response = requests.get(url, params=params)
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
        print("link to job: "+str(href)+ "\n")
        links.append(href)

print(len(links))

for link in links:
    print("link to job: "+link)
    response = requests.get(link)


