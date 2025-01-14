from ..application.applicationBuilderAbstract import ApplicationBuilder
from .directApplication  import DirectApplication

class DirectApplicationBuilder(ApplicationBuilder):
    def __init__(self):
        self.candidate_profile = None
        self.jobs = None

    def set_candidate_profile(self, profile):
        self.candidate_profile = profile

    def set_jobs_file(self, jobsFile):
        self.jobs = jobsFile

    def build_application(self):
        return DirectApplication(self.candidate_profile, self.jobs)

