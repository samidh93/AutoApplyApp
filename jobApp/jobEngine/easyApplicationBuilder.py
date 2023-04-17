from applicationBuilderAbstract import ApplicationBuilder
from applicationAbstract import Application
from jobBuilderLinkedin import JobBuilder, JobParser, Job

class EasyApplyApplicationBuilder(ApplicationBuilder):
    def __init__(self):
        self.candidate_profile = None
        self.jobs = None

    def set_candidate_profile(self, profile):
        self.candidate_profile = profile

    def set_jobs(self, jobs):
        self.jobs = jobs

    def build_application(self):
        return EasyApplyApplication(self.candidate_profile, self.jobs)

class EasyApplyApplication(Application):
    def __init__(self, candidate_profile, jobs):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Easy Apply'
    
    def ApplyForJob(self, job:Job):
        pass


