from ..application.applicationBuilderAbstract import ApplicationBuilder
from .easyApplyApplication import EasyApplyApplication

class EasyApplyApplicationBuilder(ApplicationBuilder):
    def __init__(self):
        self.candidate_profile = None
        self.jobs = None

    def set_candidate_profile(self, profile):
        self.candidate_profile = profile

    def set_jobs_file(self, jobsFile):
        self.jobsFile = jobsFile

    def set_linkedin_data(self, linkedinData):
        self.linkedinData = linkedinData

    def build_application(self):
        return EasyApplyApplication(candidate_profile = self.candidate_profile, csvJobsFile= self.jobsFile, linkedinData=self.linkedinData)



