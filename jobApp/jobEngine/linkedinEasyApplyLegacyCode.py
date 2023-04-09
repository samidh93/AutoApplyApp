from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import re
import json
import requests
import urllib
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.chrome.service import Service

class EasyApplyLinkedin:

    def __init__(self, data ,headless = False):
        """Parameter initialization"""

        self.email = data["login"]['email']
        self.password = data["login"]['password']
        self.keywords = data["login"]['keywords']
        self.location = data["login"]['location']
        self.chromedriver = data["login"]['driver_path']
        self.option = webdriver.ChromeOptions()
        if headless:
            self.option.add_argument("--headless=new")
        self.option.binary_location = data["login"]["browser_bin_location"]
        s = Service(self.chromedriver)
        self.driver = webdriver.Chrome(service=s, options=self.option)
        self.driver.implicitly_wait(30)
        self.data = data

    def login_linkedin(self):
        """This function logs into your personal LinkedIn profile"""

        # go to the LinkedIn login url
        self.driver.get("https://www.linkedin.com/login")

        # introduce email and password and hit enter
        login_email = self.driver.find_element(By.NAME,'session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_pass = self.driver.find_element(By.NAME,'session_password')
        login_pass.clear()
        login_pass.send_keys(self.password)
        login_pass.send_keys(Keys.RETURN)
        

    def getEasyApplyJobLinks(self, url, parameters) -> list:
        base_url = url
        params = parameters
        # construct the URL with the parameters
        full_url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        self.driver.get(full_url)

    def find_offers(self, max_page_to_discover=1):
        """This function finds all the offers through all the pages result of the search and filter"""
        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        total_results = self.driver.find_element(By.CLASS_NAME, "display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
        print(f"total jobs found: {total_results_int}")
        # get results for the first page
        current_page = self.driver.current_url
        results = self.driver.find_elements(By.CLASS_NAME,"jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
        # for each job add, submits application if no questions asked
        for result in results:
            print("scrolling down jobs to load all results on this page...")
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            # Find the link element by its tag name
            link_element = result.find_element_by_tag_name('a')
            # Extract the href attribute from the link element
            link_href = link_element.get_attribute('href')
            print(f"link for job {link_href}")
            #titles = result.find_elements(By.CLASS_NAME,'full-width.artdeco-entity-lockup__title.ember-view')
            #for title in titles:
            #    self.clickJobs(title)

        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            print("there are more than one jobs page")
            if max_page_to_discover>1:
                print(f"try to apply for the pages given: {max_page_to_discover}")
                # find the last page and construct url of each page based on the total amount of pages
                find_pages = self.driver.find_elements(By.CLASS_NAME,"artdeco-pagination__indicator.artdeco-pagination__indicator--number")
                total_pages = find_pages[len(find_pages)-1].text
                total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
                get_last_page = self.driver.find_element(By.XPATH,"//button[@aria-label='Page "+str(total_pages_int)+"']")
                get_last_page.send_keys(Keys.RETURN)
                last_page = self.driver.current_url
                total_jobs = int(last_page.split('start=',1)[1])
                # go through all available pages and job offers and apply
                for page_number in range(25,total_jobs+25,25):
                    self.driver.get(current_page+'&start='+str(page_number))
                    results_ext = self.driver.find_elements(By.CLASS_NAME,"occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0.ember-view")
                    for result_ext in results_ext:
                        hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                        hover_ext.perform()
                        titles_ext = result_ext.find_elements(By.CLASS_NAME,'job-card-search__title.artdeco-entity-lockup__title.ember-view')
                        for title_ext in titles_ext:
                            self.clickJobs(title_ext)

    def clickJobs(self, job_add):
        print('You are applying to the position of: ', job_add.text)
        job_add.click()

    def submit_apply(self,job_add):
        """This function submits the application for the job add found"""        
        
        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element(By.XPATH,"//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.click()
            

        # try to bypass next and inputs
            try:
                try:
                    # if next is shown
                    try:
                        phone_field = self.driver.find_elements(By.CLASS_NAME,"ember-text-field.ember-view.fb-single-line-text__input")
                        phone_field.send_keys('17666994604')
                    except:
                        pass
                    continue_job = self.driver.find_element(By.XPATH,"//button[@aria-label='Continue to next step']")
                    continue_job.click()
                    
                except:
                    print('no next..')
                    pass
                try:
                    # if another next is shown
                    continue_job = self.driver.find_element(By.XPATH,"//button[@aria-label='Continue to next step']")
                    continue_job.click()
                    
                except:
                    print('no 2 next..')
                    pass
                try:
                    # if options to select given
                    select = Select(self.driver.find_element_by_id('urn:li:fs_easyApplyFormElement:(urn:li:fs_normalized_jobPosting:2462810884,21613107,multipleChoice)'))
                    # select by visible text
                    select.select_by_visible_text('Verhandlungssicher')
                    
                except:
                    print('no options..')
                    pass
                try:
                    # if input field are demanded
                    input_field = self.driver.find_elements(By.CLASS_NAME,"ember-text-field.ember-view.fb-single-line-text__input")
                    for f in input_field:
                        f.clear()
                        f.send_keys('2')
                    
                except:
                    print('no inputs..')
                    pass
                try:
                    try:
                        phone_field = self.driver.find_elements(By.CLASS_NAME,"ember-text-field.ember-view.fb-single-line-text__input")
                        phone_field.send_keys('17666994604')
                    except:
                        pass
                    continue_job = self.driver.find_element(By.XPATH,"//button[@aria-label='Continue to next step']")
                    continue_job.click()
                    
                except:
                    print('no next..')
                    pass
                try:
                    # if review job demand
                    continue_job = self.driver.find_element(By.XPATH,"//button[@aria-label='Review your application']")
                    continue_job.click()
                    
                except:
                    print('not reviewing..')
                    pass
                finally:
                    # finally submit application
                    try:
                        phone_field = self.driver.find_elements(By.CLASS_NAME,"ember-text-field.ember-view.fb-single-line-text__input")
                        phone_field.send_keys('17666994604')
                    except:
                        pass
                    submit = self.driver.find_element(By.XPATH,"//button[@data-control-name='submit_unify']")
                    submit.send_keys(Keys.RETURN)
                    
                    try:
                        # after submit close window
                        closing = self.driver.find_element(By.XPATH,"//button[@aria-label='Dismiss']")
                        closing.click()
                        
                    except:
                        print('no close popup')
                        pass 
            # ... if not available, discard application and go to next
            except NoSuchElementException:
                print('can not apply, going to next...')
                try:
                    discard = self.driver.find_element(By.XPATH,"//button[@data-test-modal-close-btn]")
                    discard.send_keys(Keys.RETURN)
                    
                    discard_confirm = self.driver.find_element(By.XPATH,"//button[@data-test-dialog-primary-btn]")
                    discard_confirm.send_keys(Keys.RETURN)
                    
                except NoSuchElementException:
                    pass
            
        # if already applied
        except NoSuchElementException:
            print('You already applied to this job, go to next...')
            pass
        


    def close_session(self):
        """This function closes the actual session"""
        
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        """Apply to job offers"""
        self.login_linkedin()
        self.getEasyApplyJobLinks(self.data["urls"]["search_job_url"],self.data["params"] )
        self.find_offers()
        self.close_session()


if __name__ == '__main__':
    with open('jobApp/secrets/linkedin.json') as config_file:
        data = json.load(config_file)
    bot = EasyApplyLinkedin(data)
    bot.apply()