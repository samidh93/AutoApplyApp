from seleniumWrapper import WebScraper
from formFinder import FormLocator
from emailPageFinder import EmailExtractor
from jobBuilderLinkedin import JobBuilder, JobParser
from linkedinEasyApplyLegacyCode import EasyApplyLinkedin


if __name__ == "__main__":
    scraper = WebScraper('jobApp/secrets/linkedin.json', headless=False)
    jobParserObj = JobParser('jobApp/secrets/linkedin.json')
    jobParserObj.setEasyApplyFilter(True)
    bot = scraper.createJobSearchSession()
    bot.getEasyApplyJobSearchUrlResults(
        jobParserObj.base_url, jobParserObj.params)
    bot.getJobOffersListEasyApply()
