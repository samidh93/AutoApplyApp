from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
import time
import logging
from urllib.parse import urlparse
from ..config.config import UserConfig
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

logger = logging.getLogger(__name__)
""" Base class with base configuration for linkedin login, search and selenium driver"""

class LoginException(Exception):
    pass

class LinkedinSeleniumBase:
    def __init__(self, linkedin_data, driver_config_file='jobApp/secrets/config.json', default_linkedin_config = 'jobApp/secrets/sample_linkedin_user.json'):
        self._load_driver_params_from_file(driver_config_file) # for config selenium driver 
        self._load_urls_params_from_file(driver_config_file)
        self.driver = self._create_selenium_driver(driver_config_file)
        self._load_linkedin_parameters(linkedin_data, default_linkedin_config)
        self.saved_cookies = None
        
    def _load_driver_params_from_file(self, config_in):
        with open(config_in) as config_file:
            self.config = json.load(config_file)
         # driver 

    def _create_selenium_driver(self, config_file,implicit_wait=5 ):
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
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
        # load actual user data   :str
        if isinstance(source, str):
            try:
                incomingJsondata = json.loads(source)
                # Do something with the decoded data
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
        # load actual user data   :dict
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
        #logger.info(f"user data: {user_data}")
        self.email = user_data.get('email', default_user_json.get("email"))
        self.password = user_data.get('password', default_user_json.get("password"))
        # otp link
        self.otp_link = user_data.get('otp_link', default_user_json.get("otp_link"))
        # IMPORTANT ID
        self.owner_id = user_data.get('owner', default_user_json.get("owner_id"))
        logging.info(f"owner id: {self.owner_id}")
        self.created_date = user_data.get('created_date', default_user_json.get("created_date"))
        # use it for cookies
        self.field_id = user_data.get('field_id', default_user_json.get("id"))
        # Search parameters
        search_params:dict = incomingJsondata.get("search_params", default_user_json.get("search_params"))
        self.job_title = search_params.get('job', default_user_json["search_params"]["job"])
        self.location = search_params.get('location', default_user_json["search_params"]["location"])
        # extra: applications limit:
        self.applications_limit = search_params.get("limit", "10")
        # internal params
        self.start_pos=0
        self.page_num = search_params.get('pageNum', default_user_json["search_params"]["pageNum"])
        self.job_pos = search_params.get('start' , default_user_json["search_params"]["start"])
        self.filter_easy_apply = search_params.get('f_AL', default_user_json["search_params"]["f_AL"])
        self.work_type = search_params.get('f_WT', default_user_json["search_params"]["f_WT"])
        # Create params dictionary
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'f_AL': self.filter_easy_apply,
            'f_WT': self.work_type,
            'start': self.start_pos
        }


    def login_linkedin(self, save_cookies=True):
        """This function logs into your personal LinkedIn profile"""
        # try to load cookies from file if they exist
        try:
            self.driver.get(self.base_url)
            self._load_cookies_user()
            return self.driver  
        except:
            logger.info("cookies not found or could ne be loaded")
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
            time.sleep(5)
            current_url = self.driver.current_url
            logger.info(f"current url: {current_url}")
            baseRedirectUrl = "https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin"
            if not self.is_url_subset(current_url, baseRedirectUrl):
                logger.info("wrong credentials or robot check")
                self.driver.close()
                raise LoginException(f"login attempt failed, redirection not as expected url")
            if save_cookies:
                    self._save_cookies()
            logger.info("login completed")
            return self.driver

        except LoginException as e:
            logger.error(f"{e}")
            #self.driver.quit()
            raise # reraise the exception to the caller
        
    def login_linkedin_otp(self, save_cookies=True): 
        """This function logs into your personal LinkedIn profile using otp link"""
        # try to load cookies from file if they exist
        try:
            self.driver.get(self.base_url)
            self._load_cookies_user()
            return self.driver  
        except:
            logger.info("cookies not found or could ne be loaded")
        # go to the LinkedIn login url
        try: 
            logger.info(f"trying login with otp link: {self.otp_link}")
            self.driver.get(self.otp_link)
            time.sleep(5)
            current_url = self.driver.current_url
            logger.info(f"current url: {current_url}")
            baseRedirectUrl = "https://www.linkedin.com/feed/?trk=guest_homepage-basic_nav-header-signin"
            if not self.is_url_subset(current_url, baseRedirectUrl):
                logger.info("wrong credentials or robot check")
                self.driver.close()
                raise LoginException(f"login attempt failed, redirection not as expected url")
            if save_cookies:
                    self._save_cookies()
            logger.info("login completed")
            return self.driver

        except LoginException as e:
            logger.error(f"{e}")
            #self.driver.quit()
            raise # reraise the exception to the caller

    def getEasyApplyJobSearchRequestUrlResults(self, pageNum=0, start=0  ):
        self.params['start'] = start
        logger.info(f"################## getting jobs starting from {self.params['start']} ###############")
        full_url = f"{self.job_search_url}?{'&'.join([f'{k}={v}' for k, v in self.params.items()])}"
        logger.info(f"constructed url: {full_url }")
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
        logger.info('End of the session, see you later!')
        self.driver.close()
        self.driver.quit()

    def _save_cookies(self, cookies_path=UserConfig.secrets_path):
        # Save the cookies to a file
        try:
            cookies = self.driver.get_cookies()
            self.saved_cookies = cookies
            # store the cookies usign owner and field id: important to retrieve it later
            cookies_file = f"{cookies_path}/cookies_{self.owner_id}_{self.field_id}.json"
            logger.info(f"cookie saved to: {cookies_file}")
            self.saved_cookies_file = cookies_file
            # save the cookies to a JSON file
            with open(self.saved_cookies_file, 'w') as f:
                json.dump(cookies, f)
        except Exception as e:
            logger.error(f"save cookie error {e}")

    def _load_cookies_user(self, cookies_path=UserConfig.secrets_path):
        try:
            # Look for the cookies file with owner id in cookies path
            cookies_file = UserConfig.get_cookies_file(byowner=self.owner_id, byfield=self.field_id)
            if cookies_file is None:
                raise FileNotFoundError("No cookie file for user is found")
            # Load the cookies from the JSON file
            with open(cookies_file, 'r') as f:
                cookies = json.load(f)
            self.saved_cookies = cookies
            # Add the cookies to the webdriver
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            # Refresh the page to apply the cookies
            self.driver.refresh()
        except FileNotFoundError as e:
            logger.info(f"Error loading cookies: {e} , attempting direct login")
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