
from linkedinSeleniumBase import EasyApplyLinkedin, webdriver
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

 
    
    def getPortFromUrl(self, url)-> int : 
        print(f"parsing url {url} for port ")
        return urlparse(url).port

if __name__ == '__main__':
    pass