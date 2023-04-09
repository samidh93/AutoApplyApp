
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin
import json
from urllib.parse import urlparse


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

    def createLoginSession(self, writeSessionToFile=True, sessionFile="jobApp/secrets/session.json") -> EasyApplyLinkedin:
        """ create a session only for login and start detached"""
        self.loginSession = EasyApplyLinkedin(self.linked_data, self.headless, self.detached)
        self.loginSessionId = self.loginSession.driver.session_id
        self.loginCmdExecutorUrl = self.loginSession.driver.command_executor._url
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

        return self.loginSession

    def createJobSearchSession(self, attachToLoginSessionFromFile=True, SessionFile="jobApp/secrets/session.json") -> EasyApplyLinkedin:
        """ create a session only for job search and attach to the login session"""
        
        if attachToLoginSessionFromFile:
            with open(SessionFile, "r") as f:
                data = json.load(f)
        self.server_port = self.getPortFromUrl( data["session"]["cmdExecutor"])
        self.searchSession = EasyApplyLinkedin(self.linked_data, self.headless, server_port=self.server_port)
        self.searchSession.close_session()
        self.searchSession.driver.session_id  = data["session"]["id"]
        self.searchSession.driver.session_id  = data["session"]["cmdExecutor"]
        return self.searchSession
    
    def getPortFromUrl(self, url)-> int : 
        return urlparse(self.loginCmdExecutorUrl).port

if __name__ == '__main__':
    from formFinder import FormLocator
    from emailPageFinder import EmailExtractor
    from jobBuilderLinkedin import JobBuilder, JobParser
    jobParserObj = JobParser('jobApp/secrets/linkedin.json')
    scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
    scraper.bot.login_linkedin()
    scraper.bot.getEasyApplyJobSearchUrlResults(
        jobParserObj.base_url, jobParserObj.params)
    linksToApply = scraper.bot.getJobOffersListEasyApply()
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
