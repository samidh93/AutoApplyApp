from ..application.applicationBuilderAbstract import ApplicationBuilder
from .emailApplication import EmailApplication

class EmailApplicationBuilder(ApplicationBuilder):
    def __init__(self):
        self.candidate_profile = None
        self.jobs = None

    def set_candidate_profile(self, profile):
        self.candidate_profile = profile

    def set_jobs(self, jobs):
        self.jobs = jobs

    def build_application(self):
        return EmailApplication(self.candidate_profile, self.jobs)
