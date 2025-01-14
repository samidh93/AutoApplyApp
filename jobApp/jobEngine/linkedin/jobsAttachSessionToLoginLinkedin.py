
from .linkedinSeleniumBase import LinkedinSeleniumBase
import json
from urllib.parse import urlparse
import logging
logger = logging.getLogger(__name__)
'''
    attach a driver session to a previous created session from a file
'''
class JobSearchRequestSessionAttachLinkedin:
    def __init__(self, linkedin_data):
        self.linked_data = linkedin_data
        self.loginSession = None
        self.loginSessionId = None
        self.loginCmdExecutorUrl = None
        self.searchSession = None
        self.searchSessionId = None
        self.searchCmdExecutorUrl = None
        self.server_port= None

    def createJobSearchRequestSession(self, attachToLoginSessionFromFile=True, SessionFile="jobApp/secrets/session.json"):
     """ create a session only for job search and attach to the login session"""
     if attachToLoginSessionFromFile:
         logger.info("attach session using json file session data")
         with open(SessionFile, "r") as f:
             data = json.load(f)
         self.server_port = self.getPortFromUrl( data["session"]["cmdExecutor"])
         temp = data["session"]["id"]
         logger.info(f"json session id {temp}")
         logger.info(f"json server port : {self.server_port}")
         # Create a new Chrome driver and attach it to the existing session
         self.searchSession = LinkedinSeleniumBase(self.linked_data)
         self.searchSession.close_session()
         self.searchSession.driver.session_id  = data["session"]["id"]
         self.searchSession.driver.command_executor._url  = data["session"]["cmdExecutor"]
         # Open a new window and switch to it
         self.searchSession.driver.execute_script("window.open('','_blank');")
         self.searchSession.driver.switch_to.window(self.searchSession.driver.window_handles[0])
     return self.searchSession
    
    def getPortFromUrl(self, url)-> int : 
        logger.info(f"parsing url {url} for port ")
        return urlparse(url).port
