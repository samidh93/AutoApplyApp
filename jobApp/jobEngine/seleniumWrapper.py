from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import json
import os
import time
import pickle


class WebScraper:
    def __init__(self, chromeriver_path="../chromedriver", browser_bin_location='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'):

        self.chromedriver = chromeriver_path
        self.option = webdriver.ChromeOptions()
        self.option.binary_location = browser_bin_location
        s = Service(self.chromedriver)
        self.driver = webdriver.Chrome(service=s, options=self.option)

    def login_user(self, url="https://www.linkedin.com/login", username_xpath='//*[@id="username"]', password_xpath='//*[@id="password"]', user_credentials="jobApp/secrets/linkedin.json", quit_after=True):
        self.driver.get(url)
        # Load the JSON file containing the API token
        self.cwd = os.getcwd()
        self.cred_json = os.path.join(self.cwd, user_credentials)
        # Construct the path to the token.json file relative to the current working directory
        if os.path.exists(self.cred_json):
            print("linkedin.json found at:", self.cred_json)
        else:
            print("linkedin.json not found at:", self.cred_json)
        with open(self.cred_json, 'r') as f:
            cred = json.load(f)
        input_username = self.driver.find_element(By.XPATH, username_xpath)
        input_username.send_keys(cred["username"])
        input_password = self.driver.find_element(By.XPATH, password_xpath)
        input_password.send_keys(cred["password"])
        input_password.send_keys(Keys.RETURN)
        self._save_cookies()
        if quit_after:
            self.driver.quit()

    def get_redirected_page_url(self, url, by, element):
        self.driver.get(url)
        self._load_cookies()
        button = self.driver.find_element(by, element)
        button.click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        # get the URL of the newly opened page
        new_url = self.driver.current_url
        # do something with the URL
        print(new_url)
        # close the new tab and switch back to the original tab
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.quit()
        return new_url

    def _save_cookies(self, cookies_file='jobApp/secrets/cookies.json'):
        # Save the cookies to a file
        cookies = self.driver.get_cookies()
        print(cookies)
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

    scraper = WebScraper()
    # scraper.login_user()
    redirect_url = scraper.get_redirected_page_url(
        'https://www.linkedin.com/jobs/view/3521134178', 
        By.XPATH ,"//span[text()='Apply']")
    print(redirect_url)
