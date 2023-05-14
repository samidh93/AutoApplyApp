from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
import time
import json
from selenium.webdriver.chrome.service import Service


class EasyApplyLinkedin:

    def __init__(self, linkedin_data, headless=False, detached=False):
        """Parameter initialization"""
        with open(linkedin_data) as config_file:
            data = json.load(config_file)
        self.email = data["login"]['email'][1]
        self.password = data["login"]['password'][1]
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
        self.params = {
            'keywords': self.job_title,
            'location': self.location,
            'position': self.job_pos, # 25 per page
            'pageNum': self.page_num, # we increment this for next page
            'f_AL': self.filter_easy_apply # we increment this for next page
        }

        self.option = webdriver.ChromeOptions()
        if headless:
            self.option.add_argument("--headless=new")
        if detached:
            self.option.add_argument("--detached")

        self.option.binary_location = data["login"]["browser_bin_location"]
        s = Service(self.chromedriver)
        self.driver = webdriver.Chrome(service=s, options=self.option)
        self.driver.implicitly_wait(5)
        self.data = data
        self.links = []
        self.jobs = []

    def login_linkedin(self, save_cookies=False):
        """This function logs into your personal LinkedIn profile"""
        # go to the LinkedIn login url
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

    def getEasyApplyJobSearchUrlResults(self) -> list:
        print(f"getting job from page {self.params['pageNum']}")
        full_url = f"{self.base_url}?{'&'.join([f'{k}={v}' for k, v in self.params.items()])}"
        print(f"constructed url: {full_url }")
        self.driver.get(full_url)

    def getUnlockJobLinksNoLogin(self, page_to_visit=5):
        """This function finds all the offers through all the pages result of the search and filter"""
        # find the total amount of results/pages
        jobsPerPage= 0
        total_results = self.driver.find_element(
            By.CLASS_NAME, "results-context-header__job-count")
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", "").replace(".", ""))
        print(f"total jobs found: {total_results_int}")
        for page in range(page_to_visit):
            results = self.driver.find_elements(
                By.XPATH, '//*[@id="main-content"]/section[2]/ul/li' )
            # for each job add, get the link
            print(f"------------------------------------------------------------------- ")
            print(f"scrolling down the page to load all results, current result count: {len(results)}")
            print(f"current job per page count: {jobsPerPage}")
            print(f"current loop interval: {jobsPerPage} ------> {len(results)}")
            print(f"--------------------------------------------------------------------")
            for i, result in enumerate(results[jobsPerPage:]):
                hover = ActionChains(self.driver).move_to_element(result)
                hover.perform()
                time.sleep(1)
                try:
                    link_element = WebDriverWait(result, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'a')))
                    link_href = link_element.get_attribute('href')
                    print(f"link_{i} for job {link_href}")
                    self.links.append(link_href)
                    print("link added to list")
                except:
                    print("Element not found")
            jobsPerPage = jobsPerPage+25
            print(f"saved {len(self.links)} links")
        return self.links
                
    def getJobOffersListEasyApply(self, max_page_to_discover=1):
        """This function finds all the offers through all the pages result of the search and filter"""
        # find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
        total_results = self.driver.find_element(
            By.CLASS_NAME, "display-flex.t-12.t-black--light.t-normal")
        total_results_int = int(
            total_results.text.split(' ', 1)[0].replace(",", ""))
        print(f"total jobs found: {total_results_int}")
        # get results for the first page
        current_page = self.driver.current_url
        results = self.driver.find_elements(
            By.CLASS_NAME, "jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
        # for each job add, get the lnik
        print("scrolling down jobs to load all results on this page...")
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            time.sleep(0.5)
            try:
                link_element = WebDriverWait(result, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'a')))
                link_href = link_element.get_attribute('href')
                print(f"link for job {link_href}")
                self.links.append(link_href)
                print("Element found")
            except:
                print("Element not found")

            print(f"found {len(self.links)} links")
            
        # if there is more than one page, find the pages and apply to the results of each page
        if total_results_int > 24:
            print("there are more than one jobs page")
            if max_page_to_discover > 1:
                print(
                    f"try to apply for the pages given: {max_page_to_discover}")
                # find the last page and construct url of each page based on the total amount of pages
                find_pages = self.driver.find_elements(
                    By.CLASS_NAME, "artdeco-pagination__indicator.artdeco-pagination__indicator--number")
                total_pages = find_pages[len(find_pages)-1].text
                total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
                get_last_page = self.driver.find_element(
                    By.XPATH, "//button[@aria-label='Page "+str(total_pages_int)+"']")
                get_last_page.send_keys(Keys.RETURN)
                last_page = self.driver.current_url
                total_jobs = int(last_page.split('start=', 1)[1])
                # go through all available pages and job offers and apply
                for page_number in range(25, total_jobs+25, 25):
                    self.driver.get(current_page+'&start='+str(page_number))
                    results_ext = self.driver.find_elements(
                        By.CLASS_NAME, "occludable-update.artdeco-list__item--offset-4.artdeco-list__item.p0.ember-view")
                    for result_ext in results_ext:
                        hover_ext = ActionChains(
                            self.driver).move_to_element(result_ext)
                        hover_ext.perform()
                        titles_ext = result_ext.find_elements(
                            By.CLASS_NAME, 'job-card-search__title.artdeco-entity-lockup__title.ember-view')
                        for title_ext in titles_ext:
                            self.clickOnJob(title_ext)
        return self.links

    def clickOnJob(self, job_add):
        print('You are applying to the position of: ', job_add.text)
        job_add.click()

    def submit_apply(self, job_add):
        """This function submits the application for the job add found"""

        # click on the easy apply button, skip if already applied to the position
        try:
            in_apply = self.driver.find_element(
                By.XPATH, "//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.click()

        # try to bypass next and inputs
            try:
                try:
                    # if next is shown
                    try:
                        phone_field = self.driver.find_elements(
                            By.CLASS_NAME, "ember-text-field.ember-view.fb-single-line-text__input")
                        phone_field.send_keys(self.data["login"]["phone"])
                    except:
                        pass
                    continue_job = self.driver.find_element(
                        By.XPATH, "//button[@aria-label='Continue to next step']")
                    continue_job.click()

                except:
                    print('no next..')
                    pass
                try:
                    # if another next is shown
                    continue_job = self.driver.find_element(
                        By.XPATH, "//button[@aria-label='Continue to next step']")
                    continue_job.click()

                except:
                    print('no 2 next..')
                    pass
                try:
                    # if options to select given
                    select = Select(self.driver.find_element_by_id(
                        'urn:li:fs_easyApplyFormElement:(urn:li:fs_normalized_jobPosting:2462810884,21613107,multipleChoice)'))
                    # select by visible text
                    select.select_by_visible_text('Verhandlungssicher')

                except:
                    print('no options..')
                    pass
                try:
                    # if input field are demanded
                    input_field = self.driver.find_elements(
                        By.CLASS_NAME, "ember-text-field.ember-view.fb-single-line-text__input")
                    for f in input_field:
                        f.clear()
                        f.send_keys('2')

                except:
                    print('no inputs..')
                    pass
                try:
                    try:
                        phone_field = self.driver.find_elements(
                            By.CLASS_NAME, "ember-text-field.ember-view.fb-single-line-text__input")
                        phone_field.send_keys(self.data["login"]["phone"])
                    except:
                        pass
                    continue_job = self.driver.find_element(
                        By.XPATH, "//button[@aria-label='Continue to next step']")
                    continue_job.click()

                except:
                    print('no next..')
                    pass
                try:
                    # if review job demand
                    continue_job = self.driver.find_element(
                        By.XPATH, "//button[@aria-label='Review your application']")
                    continue_job.click()

                except:
                    print('not reviewing..')
                    pass
                finally:
                    # finally submit application
                    try:
                        phone_field = self.driver.find_elements(
                            By.CLASS_NAME, "ember-text-field.ember-view.fb-single-line-text__input")
                        phone_field.send_keys(self.data["login"]["phone"])
                    except:
                        pass
                    submit = self.driver.find_element(
                        By.XPATH, "//button[@data-control-name='submit_unify']")
                    submit.send_keys(Keys.RETURN)

                    try:
                        # after submit close window
                        closing = self.driver.find_element(
                            By.XPATH, "//button[@aria-label='Dismiss']")
                        closing.click()

                    except:
                        print('no close popup')
                        pass
            # ... if not available, discard application and go to next
            except NoSuchElementException:
                print('can not apply, going to next...')
                try:
                    discard = self.driver.find_element(
                        By.XPATH, "//button[@data-test-modal-close-btn]")
                    discard.send_keys(Keys.RETURN)

                    discard_confirm = self.driver.find_element(
                        By.XPATH, "//button[@data-test-dialog-primary-btn]")
                    discard_confirm.send_keys(Keys.RETURN)

                except NoSuchElementException:
                    pass

        # if already applied
        except NoSuchElementException:
            print('You already applied to this job, go to next...')
            pass

    def get_official_job_page_url(self, url, by, applyTag, by_, easyApplyTag):
        self.driver.get(url)
        try:
            button = self.driver.find_element(by, applyTag)
        except:
            print("button apply not found")
            return self._easy_apply(by_, easyApplyTag)
        button.click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        # get the URL of the newly opened page
        new_url = self.driver.current_url
        # do something with the URL
        print(new_url)
        # close the new tab and switch back to the original tab
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        # self.driver.quit()
        return new_url

    def close_session(self):
        """This function closes the actual session"""
        print('End of the session, see you later!')
        self.driver.close()

    def apply(self):
        """Apply to job offers"""
        self.login_linkedin()
        self.getEasyApplyJobSearchUrlResults()
        self.getJobOffersListEasyApply()
        self.close_session()

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
    bot = EasyApplyLinkedin('jobApp/secrets/linkedin.json')
    bot.getEasyApplyJobSearchUrlResults()
    bot.getUnlockJobLinksNoLogin()