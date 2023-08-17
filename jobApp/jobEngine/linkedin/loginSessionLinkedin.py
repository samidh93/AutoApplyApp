
from .linkedinSeleniumBase import LinkedinSeleniumBase
import json
from urllib.parse import urlparse

'''
    create a linked login session, save driver session in a file
    and keep the browser alive
'''
class LoginSessionLinkedCreator:
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


    def createLoginSession(self, writeSessionToFile, sessionFile="jobApp/secrets/session.json"):
        """ create a session only for login and start detached"""
        self.loginSession = LinkedinSeleniumBase(self.linked_data, self.headless)
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

 
