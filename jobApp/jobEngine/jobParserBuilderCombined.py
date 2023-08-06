from jobBuilderLinkedin import JobBuilder
from jobParserLinkedin import JobParser

class JobParserBuilder:
    def __init__(self, config_file, csv_links_file_out, jobs_file_out, num_of_pages_to_visit):
        self.csv_links_file_out, self.jobs_file_out = csv_links_file_out, jobs_file_out
        self.jobParserObj = JobParser(config_file,csv_links_file_out)
        self.Num_pages = num_of_pages_to_visit

    def generateJobs(self):
        links, html_sources = self.jobParserObj.createListOfLinksDriver(self.Num_pages)
        self.jobBuilderObj= JobBuilder(links, "onsite", self.csv_links_file_out, self.jobs_file_out)
        self.jobBuilderObj.createJobObjectList(html_sources)

