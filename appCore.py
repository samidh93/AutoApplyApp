from jobApp.jobScraperLinkedinMicroService import JobScraperLinkedinMicroService
from jobApp.linkedinEasyApplyMicroService import easyApplyMicroService
from jobApp.loginSessionLinkedinMicroService import LoginSessionLinkedCreator, LoginException
from jobApp.jobEngine.config.config import UserConfig
import time
import logging
from dotenv import load_dotenv
import os
import logging_config  # Import the logging configuration
import json
logger = logging.getLogger(__name__)


class appCreatorLinkedin:
    def __init__(self, incomingData: str = None, unique_id=None) -> None:
        logger.info("initiating app Creator Linkedin")
        print("init app")
        self.incomingData = incomingData
        self.unique_id = unique_id

    def tryCredentialsLinkedin(self):
        self.linkedSessionCreatorService = LoginSessionLinkedCreator(
            linkedin_data=self.incomingData)
        try:
            verified, cookies = self.linkedSessionCreatorService.attemptLogin()
            return verified, cookies
        except LoginException as E:
            logger.error(f"exception: {E}")
            raise

    def getCookiesLinkedin(self, unique_id):
        try:
            result = UserConfig().find_jobs_result_json_file(unique_id)
            if result is None:
                return 0
            result_count = result.get("job_count", 0)
            jobs_dict = result.get("jobs", None)
            logger.info("number of succeded jobs: %d", result_count)
            return result_count, jobs_dict
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise

    def searchJobs(self):
        self.linkedinJobCollector = JobScraperLinkedinMicroService(
            linkedin_data=self.incomingData)
        try:
            jobCount, jobLinks = self.linkedinJobCollector.run_service()
            logger.info("number searched jobs found: %d", len(jobLinks))
            return jobCount, jobLinks
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise

    def getFoundJobs(self, unique_id=None):
        self.linkedinJobCollector = JobScraperLinkedinMicroService(
            linkedin_data=self.incomingData)
        try:
            jobCount = self.linkedinJobCollector.get_jobs_found()
            logger.info("number jobs found: %d", jobCount)
            return jobCount
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise

    def getSearchedJobs(self, unique_id):
        try:
            result = UserConfig().find_jobs_result_json_file(unique_id)
            if result is None:
                return 0
            result_count = result.get("job_count", 0)
            jobs_dict = result.get("jobs", None)
            logger.info("number of succeded jobs: %d", result_count)
            return result_count, jobs_dict
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise

    def applyJobs(self):
        self.linkedinJobApply = easyApplyMicroService(
            linkedinConfig=self.incomingData)
        try:
            jobCount, jobList = self.linkedinJobApply.run_service()
            logger.info("number jobs to apply for on request: %d", jobCount)
            return jobCount, jobList
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise

    def getAppliedJobs(self, unique_id):
        try:
            result = UserConfig().find_jobs_result_json_file(unique_id)
            if result is None:
                return 0
            result_count = result.get("job_count", 0)
            jobs_dict = result.get("jobs", None)
            logger.info("number of succeded jobs: %d", result_count)
            return result_count, jobs_dict
        except Exception as E:
            logger.error(f"exception: {str(E)}")
            raise

def createRequest(file_path):
    # Load json file
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def run_multiple_requests(json_files_list):
    for file in json_files_list:
        data = createRequest(file)
        testapp = appCreatorLinkedin(data)
        #testapp.tryCredentialsLinkedin()
        testapp.searchJobs()
        testapp.applyJobs()

if __name__ == "__main__":
    zayneb_file = "input/zayneb_dhieb.json"
    sami_file = "input/sami_dhiab.json"
    files = [zayneb_file]
    run_multiple_requests(files)

