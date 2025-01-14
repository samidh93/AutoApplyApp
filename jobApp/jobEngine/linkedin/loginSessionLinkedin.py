
from .linkedinSeleniumBase import LinkedinSeleniumBase, LoginException
import json
from urllib.parse import urlparse
import logging
logger = logging.getLogger(__name__)
'''
    create a linked login session, save driver session in a file
    and keep the browser alive
'''
class LoginSessionLinkedCreator:
    def __init__(self, linkedin_data):
        self.linked_data = linkedin_data
        self.loginSession = None
        self.loginSessionId = None
        self.loginCmdExecutorUrl = None
        self.searchSession = None
        self.searchSessionId = None
        self.searchCmdExecutorUrl = None
        self.server_port= None

    def attemptLogin(self):
        """ attempt a login with provided credentials"""
        try:
            self.loginSession = LinkedinSeleniumBase(self.linked_data)
            self.loginSession.login_linkedin()   
            self.user_cookies = self.loginSession.saved_cookies
            if len(self.user_cookies)>0:
                logger.info(f"logged using cookie success")
            return True, self.user_cookies
        except LoginException as E:
            logger.error(f"exception: {E}")
            raise
            
      
    def createLoginSession(self, writeSessionToFile, sessionFile="jobApp/secrets/session.json"):
        """ create a session only for login and start detached"""
        self.loginSession = LinkedinSeleniumBase(self.linked_data)
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
        # Keep the old session alive
        #input("------------------------------   Press Enter to quit  ------------------------------")
        while True:
            pass
        return self.loginSession

    def getPortFromUrl(self, url)-> int : 
        print(f"parsing url {url} for port ")
        return urlparse(url).port

if __name__ == '__main__':
    pass

 
