from gmail import Gmail
from candidateProfile import CandidateProfile, ChatGPT
from jobBuilderLinkedin import JobBuilder, JobParser, Job

from abc import ABC, abstractmethod

class ApplicationBuilder(ABC):
    @abstractmethod
    def set_candidate_profile(self, profile):
        pass

    @abstractmethod
    def set_jobs(self, jobs):
        pass

    @abstractmethod
    def build_application(self):
        pass

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

class DirectApplicationBuilder(ApplicationBuilder):
    def __init__(self):
        self.candidate_profile = None
        self.jobs = None

    def set_candidate_profile(self, profile):
        self.candidate_profile = profile

    def set_jobs(self, jobs):
        self.jobs = jobs

    def build_application(self):
        return DirectApplication(self.candidate_profile, self.jobs)
    
class Application(ABC):
    def __init__(self, candidate: CandidateProfile, jobOffers:list[Job]) -> None:
        self.candidate = candidate
        self.jobs_to_apply_for = jobOffers

    @abstractmethod
    def ApplyForJob(self, job:Job):
        pass

    @abstractmethod
    def ApplyForAll(self):
        pass

class EmailApplication(Application):
    def __init__(self, candidate_profile: CandidateProfile, jobs: list[Job]):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Email'
    
    def ApplyForJob(self, job: Job):
        print(f"sending email application for {job.job_title} at {job.company_name} in {job.job_location}")
        gmail = Gmail('jobApp/secrets/credentials.json', 'jobApp/secrets/token.json' )
        gmail.send_email_with_attachments(f'{self.candidate_profile.email}',f'{job.company_email}',  f'job application as {job.job_title} at {job.company_name} in {job.job_location}', self.generateApplicationEmail(job), [self.candidate.resume.file_path])
        
    def generateApplicationEmail(self, job:Job):
        candidate_resume= self.candidate.extract_resume_plain_text()
        job_title, company, location =job.job_title, job.company_name, job.job_location
        query = f"create a job application email for the job {job_title} at {company} in {location}. \
        use the candidate resume below to extract his personal infos like firstname, lastname, adress, \
        phone number and email, outline his experience, education and skills. \n {candidate_resume}"
        chatgpt = ChatGPT("jobApp/secrets/openai.json")
        email_tosend = chatgpt.ask(query)
        job.applied = True
        return email_tosend

class EasyApplyApplication(Application):
    def __init__(self, candidate_profile, jobs):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Easy Apply'

class DirectApplication(Application):
    def __init__(self, candidate_profile, jobs):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Direct'

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
    pass