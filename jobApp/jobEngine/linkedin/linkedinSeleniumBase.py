from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import time
import logging
from urllib.parse import urlparse


logger = logging.getLogger(__name__)
""" Base class with base configuration for linkedin login, search and selenium driver"""

class LoginException(Exception):
    pass

class LinkedinSeleniumBase:
    def __init__(self, linkedin_data, driver_config_file='jobApp/secrets/config.json', default_linkedin_config = 'jobApp/secrets/sample_linkedin_user.json'):
        self._load_driver_params_from_file(driver_config_file) # for config selenium driver 
        self._load_urls_params_from_file(driver_config_file)
        self.driver = self._create_selenium_driver(headless=self.headless, detached=self.detached)
        self._load_linkedin_parameters(linkedin_data, default_linkedin_config)

    def _load_driver_params_from_file(self, config_in):
        with open(config_in) as config_file:
            data = json.load(config_file)
         # driver
        self.chromedriver = data["driver"]['driver_path']
        self.headless = data["driver"]['headless']
        self.detached = data["driver"]['detached']

    def _create_selenium_driver(self, headless, detached, implicit_wait=5 ):
        option = webdriver.ChromeOptions()
        if headless:
            option.add_argument("--headless=new")
        if detached:
            option.add_argument("--detached")
        s = Service(self.chromedriver)
        driver = webdriver.Chrome(service=s, options=option)
        driver.implicitly_wait(implicit_wait)
        return driver
    
    def _load_urls_params_from_file(self, config_in):
        with open(config_in) as config_file:
            data = json.load(config_file)
        # urls
        self.base_url = data["urls"]['linkedin_base_url']
        self.login_url = data["urls"]['linkedin_login_url']
        self.job_search_url = data["urls"]['linkedin_JobSearchRequest_url']

    # better version
    def parseIncomingDataAsJson(self, source, defaultUser):
        # load default user (bypass credentials for debug)
        if isinstance(defaultUser, str): 
            # If source is a string, assume it's a file path
            try:
                with open(defaultUser, 'r') as file:
                    default_user_json:dict = json.load(file)
            except FileNotFoundError:
                raise FileNotFoundError("default user File not found")    
        # load actual user data   
        if isinstance(source, str):
            # If source is a string, assume it's a file path
            try:
                with open(source, 'r') as file:
                    incomingJsondata = json.load(file)
            except FileNotFoundError:
                raise FileNotFoundError("File not found")
        elif isinstance(source, dict):
            # If source is a dictionary, assume it's a JSON object
            incomingJsondata = source
        else:
            raise ValueError("Invalid source type")
        return incomingJsondata, default_user_json
    
    def _load_linkedin_parameters(self, source, defaultUser):
        # load incoming req data
        incomingJsondata, default_user_json = self.parseIncomingDataAsJson(source, defaultUser)
        # User data
        user_data:dict = incomingJsondata.get("user", default_user_json.get("user"))
        self.email = user_data.get('email', default_user_json.get("email"))
        self.password = user_data.get('password', default_user_json.get("password"))
        # IMPORTANT ID
        self.owner_id = user_data.get('_owner', default_user_json.get("owner_id"))
        self.created_date = user_data.get('created_date', default_user_json.get("created_date"))
        self.field_id = user_data.get('field_id', default_user_json.get("id"))
        # Search parameters
        search_params:dict = incomingJsondata.get("search_params", default_user_json.get("search_params"))
        self.job_title = search_params.get('job', default_user_json["search_params"]["job"])
        self.location = search_params.get('location', default_user_json["search_params"]["location"])
        # internal params
        self.start_pos=0
        self.page_num = search_params.get('pageNum', default_user_json["search_params"]["pageNum"])
        self.job_pos = search_params.get('start' , default_user_json["search_params"]["start"])
        self.filter_easy_apply = search_params.get('f_AL', default_user_json["search_params"]["f_AL"])
        # Create params dictionary
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'f_AL': self.filter_easy_apply,
            'start': self.start_pos
        }
        # extra: applications limit:
        self.applications_limit =incomingJsondata["candidate"]["limit"]

    def login_linkedin(self, save_cookies=True):
        """This function logs into your personal LinkedIn profile"""
        # try to load cookies from file if they exist
        try:
            self.driver.get(self.base_url)
            self._load_cookies()
            return self.driver  
        except:
            print("cookies not found or could ne be loaded")
        # go to the LinkedIn login url
        try: 
            self.driver.get(self.login_url)
            # introduce email and password and hit enter
            login_email = self.driver.find_element(By.NAME, 'session_key')
            login_email.clear()
            login_email.send_keys(self.email)
            login_pass = self.driver.find_element(By.NAME, 'session_password')
            login_pass.clear()
            login_pass.send_keys(self.password)
            login_pass.send_keys(Keys.RETURN)
            #time.
            current_url = self.driver.current_url
            baseRedirectUrl = "https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin"
            if not self.is_url_subset(current_url, baseRedirectUrl):
                print("wrong credentials or robot check")
                #raise LoginException(f"login attempt failed, redirection not as expected url")
                time.sleep(10)
            if save_cookies:
                    self._save_cookies()
            return self.driver

        except LoginException as e:
            logger.error(f"{e}")
            #self.driver.quit()
            raise # reraise the exception to the caller


    def getEasyApplyJobSearchRequestUrlResults(self, pageNum=0, start=0  ):
        self.params['start'] = start
        print(f"################## getting jobs starting from {self.params['start']} ###############")
        full_url = f"{self.job_search_url}?{'&'.join([f'{k}={v}' for k, v in self.params.items()])}"
        print(f"constructed url: {full_url }")
        self.driver.get(self.base_url)
        for cookie in self.saved_cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        self.driver.get(full_url)
        return self.driver
 
    def getCurrentSeleniumDriver(self):
        return self.driver

  
    def close_session(self):
        """This function closes the actual session"""
        print('End of the session, see you later!')
        self.driver.close()
        self.driver.quit()

    def _save_cookies(self, cookies_file='jobApp/secrets/cookies.json'):
        # Save the cookies to a file
        cookies = self.driver.get_cookies()
        self.saved_cookies = cookies
        # print(cookies)
        self.saved_cookies_file = cookies_file
        # save the cookies to a JSON file
        with open(self.saved_cookies_file, 'w') as f:
            json.dump(cookies, f)

    def _load_cookies(self, cookies_file='jobApp/secrets/cookies.json'):
        try:
            # load the cookies from the JSON file
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)
            self.saved_cookies= cookies
            # add the cookies to the webdriver
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            # Refresh the page to apply the cookie
            self.driver.refresh()
        except Exception as e:
            print("error cookies: ", e)
            raise


    def is_url_subset(self, url, base_url):
        # Parse the URLs
        parsed_url = urlparse(url)
        parsed_base_url = urlparse(base_url)

        # Compare the scheme and domain
        if parsed_url.scheme != parsed_base_url.scheme or parsed_url.netloc != parsed_base_url.netloc:
            return False

        # Check if the path of 'url' starts with the path of 'base_url'
        return parsed_url.path.startswith(parsed_base_url.path)

if __name__ == '__main__':
    pass