from bs4 import BeautifulSoup
import json
import requests
from linkedinSeleniumBase import EasyApplyLinkedin,webdriver
from selenium.webdriver.common.by import By

class FormFillBase:
    def __init__(self, form_json_template= 'jobApp/secrets/form.json', url=None):
        if form_json_template:
            self.form_data = self._load_form_template(form_json_template)
        self.inputs = []
        self.selenium = EasyApplyLinkedin('jobApp/secrets/linkedin.json')
        self.driver= self.selenium.driver
        self.url = None or url

    def setUrl(self, url):
        self.url = url

    def _load_form_template(self, form_json):
        with open(form_json, "r") as f:
            form_data = json.load(f)
            #self.print_nested(form_data)
            return form_data
        
    def get_max_depth(self, json_obj):
        # base case: if json_obj is not a dictionary, return 0
        if not isinstance(json_obj, dict):
            return 0
        # recursive case: find the maximum depth of the nested dictionaries
        max_depth = 0
        for key, value in json_obj.items():
            depth = self.get_max_depth(value)
            if depth > max_depth:
                max_depth = depth
        # return the maximum depth plus 1
        return max_depth + 1
    
    # print all nested key-value pairs up to the maximum depth
    def print_nested(self, obj, depth=1, parent_key=''):
        max_depth = self.get_max_depth(obj)
        # base case: if depth exceeds max_depth, return
        if depth > max_depth:
            return
        # recursive case: iterate over the keys and values in the object
        for key, value in obj.items():
            # construct the full key path including the parent key
            full_key = f"{parent_key}.{key}" if parent_key else key
            
            # if the value is a nested dictionary, recursively print its keys and values
            if isinstance(value, dict):
                self.print_nested(value, depth=depth+1, parent_key=full_key)
            else:
                # print the key-value pair
                print(f"{full_key}: {value}")

    def find_nested(self,obj, depth=1, parent_key='', search_key=''):
        max_depth = self.get_max_depth(obj)
        # base case: if depth exceeds max_depth, return False
        if depth > max_depth:
            return False
        
        # recursive case: iterate over the keys and values in the object
        for key, value in obj.items():
            # construct the full key path including the parent key
            full_key = f"{parent_key}.{key}" if parent_key else key
            
            # if the key matches the search key, print the key-value pair and return True
            if key in search_key.lower():
                print(f"search_key found {search_key.lower()}")
                print(f"{key}: {value}")
                return True, value
            
            # if the value is a nested dictionary, recursively search for the key
            if isinstance(value, dict):
                found, value = self.find_nested(value, depth=depth+1, parent_key=full_key, search_key=search_key)
                if found:
                    return True, value
        
        # if the search key was not found in this level of the object, return False
        return False
    
    def findFormOnHtml(self, html):
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        # Find the first form element within the HTML
        form = soup.find('form')
        if form:
            # Return the form element if found
            print(f"form found within the HTML ")
            return True
        else:
            # Raise an exception if no form element was found
            print("No form element found within the HTML")
        return False

    def getFormInputTags(self,url):
        input_names = []
        response = requests.get(url)
        html = response.text
        if not self.findFormOnHtml(html):
            return 
        # parse the HTML using Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        # find all input tags inside the form
        form_inputs = soup.form.find_all('input')
        # print the input tags
        for input_tag in form_inputs:
            #print(input_tag)
            if 'name' in input_tag.attrs:
                print(input_tag['name'])
                input_names.append(input_tag)
        self.inputs = input_names
        return input_names
    def sendKeyValue(self, key, value):
        self.driver.find_element(By.NAME,key).send_keys(value)

    def submitForm(self):
        self.driver.find_element(By.CSS_SELECTOR,'submit').submit()

    def fillForm(self, inputs:list):
        if inputs is None:
            inputs= self.inputs
        for input in inputs:
            print(input["name"])
            found,value =  self.find_nested(obj=self.form_data, search_key=input["name"])
            if found:
                name = input["name"]
                print(f"{value} will be sent to {name}")
                #self.sendKeyValue(name, 0)
        self.submitForm()

if __name__ == '__main__':
    url = "https://carriere.deskeo.fr/jobs/2294634-architecte-d-interieur-chef-fe-de-projet-cdi/applications/new?promotion=644813-trackable-share-link-annonce-linkedin-archi-cdi"
    url_1 = "https://octiva.recruitee.com/o/senior-project-manager/c/new?source=LinkedIn"
    formHandle = FormFillBase()
    formHandle.getFormInputTags(url)
    formHandle.fillForm(None)
