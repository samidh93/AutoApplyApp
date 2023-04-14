from emailApplicationBuilder import EmailApplicationBuilder
from easyApplicationBuilder import EasyApplyApplicationBuilder
from directApplicationBuilder import DirectApplicationBuilder


class ApplicationDirector:
    def __init__(self):
        self.builder = None

    def construct_application(self, candidate_profile, jobs, application_type):
        if application_type == 'Email':
            self.builder = EmailApplicationBuilder()
        elif application_type == 'Easy Apply':
            self.builder = EasyApplyApplicationBuilder()
        elif application_type == 'Direct':
            self.builder = DirectApplicationBuilder()
        else:
            raise ValueError('Invalid application type')

        self.builder.set_candidate_profile(candidate_profile)
        self.builder.set_jobs(jobs)

        return self.builder.build_application()



if __name__ == '__main__':
    from candidateProfile import CandidateProfile
    from job import Job
    candidate = CandidateProfile(resume_path='jobApp/data/zayneb_dhieb_resume_english.pdf', firstname="zayneb", lastname="dhieb", email="dhiebzayneb89@gmail.com")
    jobs = [Job(1, None, "title", "homejob", "home", None, "", company_email="sami.dhiab.x@gmail.com")]
    AppDirector = ApplicationDirector()
    emailApply = AppDirector.construct_application(candidate,jobs, "Email")
    emailApply.ApplyForJob(jobs[0])