from seleniumWrapper import WebScraper
from formFinder import FormLocator
from emailPageFinder import EmailExtractor
from jobBuilderLinkedin import JobBuilder, JobParser
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin


if __name__ == "__main__":
    scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
    #jobParserObj = JobParser('jobApp/secrets/linkedin.json')
    bot = scraper.createJobSearchSession()
    #bot.getEasyApplyJobSearchUrlResults()
    #bot.getJobOffersListEasyApply()
