from seleniumWrapper import WebScraper
from formFinder import FormLocator
from emailPageFinder import EmailExtractor
from jobBuilderLinkedin import JobBuilder, JobParser
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin
import threading


if __name__ == "__main__":
    login_task_finished = threading.Event()
    loginbot = WebScraper('jobApp/secrets/linkedin.json', headless=False)
    bot = loginbot.createLoginSession(login_task_finished)
