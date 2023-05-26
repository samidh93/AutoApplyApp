
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin, webdriver
import json
from urllib.parse import urlparse
import threading


class WebScraper:
    def __init__(self, linkedin_data, headless=False, detached= False):
        self.linked_data = linkedin_data
        self.headless = headless
        self.detached = detached
        self.loginSession = None
        self.loginSessionId = None
        self.loginCmdExecutorUrl = None
        self.searchSession = None
        self.searchSessionId = None
        self.searchCmdExecutorUrl = None
        self.server_port= None


    def createLoginSession(self, login_task_finished=None,login_task_killed = False, writeSessionToFile=True, sessionFile="jobApp/secrets/session.json") -> EasyApplyLinkedin:
        """ create a session only for login and start detached"""
        self.loginSession = EasyApplyLinkedin(self.linked_data, self.headless)
        self.loginSession.login_linkedin()
        self.loginSessionId = self.loginSession.driver.session_id
        self.loginCmdExecutorUrl = self.loginSession.driver.command_executor._url
        self.loginSession.driver.command_executor.keep_alive  = True
        self.server_port = self.getPortFromUrl(self.loginCmdExecutorUrl)
        new_data = {
            "session": {
                "id": self.loginSessionId,
                "cmdExecutor": self.loginCmdExecutorUrl
            }
        }
        if writeSessionToFile:
            with open(sessionFile, "w") as f:
                 json.dump(new_data, f)
        
        #login_task_finished.set()
        # Keep the old session alive
        #input("------------------------------   Press Enter to quit  ------------------------------")
        while True:
            login_task_finished.set()
            if login_task_killed:
                break


        return self.loginSession

    def createJobSearchSession(self, attachToLoginSessionFromFile=True, SessionFile="jobApp/secrets/session.json") -> EasyApplyLinkedin:
        """ create a session only for job search and attach to the login session"""
        if attachToLoginSessionFromFile:
            print("attach session using json file session data")
            with open(SessionFile, "r") as f:
                data = json.load(f)
            self.server_port = self.getPortFromUrl( data["session"]["cmdExecutor"])
            temp = data["session"]["id"]
            print(f"json session id {temp}")
            print(f"json server port : {self.server_port}")
            # Create a new Chrome driver and attach it to the existing session
            self.searchSession = EasyApplyLinkedin(self.linked_data, self.headless)
            self.searchSession.close_session()
            self.searchSession.driver.session_id  = data["session"]["id"]
            self.searchSession.driver.command_executor._url  = data["session"]["cmdExecutor"]
            # Open a new window and switch to it
            self.searchSession.driver.execute_script("window.open('','_blank');")
            self.searchSession.driver.switch_to.window(self.searchSession.driver.window_handles[0])
        else:
            print("using class members variables not json file..")
            self.searchSession = EasyApplyLinkedin(self.linked_data, self.headless)
            self.searchSession.close_session()
            self.searchSession.driver.session_id =  self.loginSession.driver.session_id 
            self.searchSession.driver.command_executor._url = self.loginSession.driver.command_executor._url 
        return self.searchSession
    
    def getPortFromUrl(self, url)-> int : 
        print(f"parsing url {url} for port ")
        return urlparse(url).port

if __name__ == '__main__':
    from formFinder import FormLocator
    from emailPageFinder import EmailExtractor
    from jobBuilderLinkedin import JobBuilder, JobParser
    jobParserObj = JobParser('jobApp/secrets/linkedin.json')
    jobParserObj.setEasyApplyFilter(True)
    bot = WebScraper('jobApp/secrets/linkedin.json', headless=False)
    loginBot = bot.createLoginSession()

    scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
    searchBot = scraper.createJobSearchSession(attachToLoginSessionFromFile=True)
    searchBot.getEasyApplyJobSearchUrlResults(
        jobParserObj.base_url, jobParserObj.params)
    linksToApply  = searchBot.getJobOffersListEasyApply()

    # generate all types of job application ( direct and easy apply )
    # jobs = jobParserObj.generateLinksPerPage(1)
    jobber = JobBuilder(links=linksToApply)
    joboffers = jobber.createJobObjectList()

    for j in joboffers:
        # redirect_url = scraper.get_official_job_page_url(
        #    j.job_url,
        #    By.XPATH, "//span[text()='Apply']", By.XPATH, '//span[@class="artdeco-button__text" and text()="Easy Apply"]')
        print(j.job_url)
        print(
            f"emails extracted { EmailExtractor(j.job_url).extract_emails()}")
        # FormLocator(j.job_url).locate_form()
