from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json

""" Base class with base configuration for linkedin login, search and selenium driver"""

class LinkedinSeleniumBase:

    def __init__(self, linkedin_data_file, headless=False, detached=False):
        self._load_linked_parameters_from_file(linkedin_data_file)
        self.driver = self._create_selenium_driver(headless=headless, detached=detached)
    
    def _load_linked_parameters_from_file(self, config_in):
        with open(config_in) as config_file:
            data = json.load(config_file)
        self.email = data["login"]['email'][0]
        self.password = data["login"]['password'][0]
        self.keywords = data["login"]['keywords']
        self.location = data["login"]['location']
        self.chromedriver = data["login"]['driver_path']
        # params
        self.base_url = data["urls"]['search_job_url']
        self.page_num = data["params"]['pageNum']
        self.job_title= data["login"]['keywords']
        self.location = data["login"]['location']
        self.job_pos = data["params"]['start']
        self.filter_easy_apply = data["params"]['f_AL']
        self.start_pos=0
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'f_AL': self.filter_easy_apply, # we increment this for next page
            'start': self.start_pos
        }
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


    def login_linkedin(self, save_cookies=False):
        """This function logs into your personal LinkedIn profile"""
        # go to the LinkedIn login url
        try: 
            self.driver.get("https://www.linkedin.com/login")
            # introduce email and password and hit enter
            login_email = self.driver.find_element(By.NAME, 'session_key')
            login_email.clear()
            login_email.send_keys(self.email)
            login_pass = self.driver.find_element(By.NAME, 'session_password')
            login_pass.clear()
            login_pass.send_keys(self.password)
            login_pass.send_keys(Keys.RETURN)
            if save_cookies:
                self._save_cookies()
            return True
        except Exception as e:
            print("exception:", e)
            return False


    def getEasyApplyJobSearchUrlResults(self, pageNum=0, start=0  ):
        self.params['start'] = start
        print(f"################## getting jobs starting from {self.params['start']} ###############")
        full_url = f"{self.base_url}?{'&'.join([f'{k}={v}' for k, v in self.params.items()])}"
        print(f"constructed url: {full_url }")
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
        # print(cookies)
        self.saved_cookies = cookies_file
        # save the cookies to a JSON file
        with open(self.saved_cookies, 'w') as f:
            json.dump(cookies, f)

    def _load_cookies(self, cookies_file='jobApp/secrets/cookies.json'):
        # load the cookies from the JSON file
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
        # add the cookies to the webdriver
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        # Refresh the page to apply the cookie
        self.driver.refresh()

 

if __name__ == '__main__':
    pass