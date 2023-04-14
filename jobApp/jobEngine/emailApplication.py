from applicationAbstract import Application
from candidateProfile import CandidateProfile, ChatGPT
from jobBuilderLinkedin import JobBuilder, JobParser, Job
from gmail import Gmail

class EmailApplication(Application):
    def __init__(self, candidate_profile: CandidateProfile, jobs: list[Job]):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Email'
    
    def ApplyForJob(self, job: Job):
        print(f"sending email application for {job.job_title} at {job.company_name} in {job.job_location}")
        #TODO: put threadpool if email is a list
        gmail = Gmail('jobApp/secrets/credentials.json', 'jobApp/secrets/token.json' )
        gmail.send_email_with_attachments(f'{self.candidate_profile.email}',f'{job.company_email}',  f'job application as {job.job_title} at {job.company_name} in {job.job_location}', self.generateApplicationEmail(job), [self.candidate_profile.resume.file_path])
        
    def generateApplicationEmail(self, job:Job):
        candidate_resume= self.candidate_profile.extract_resume_plain_text()
        job_title, company, location =job.job_title, job.company_name, job.job_location
        query = f"create a job application email for the job {job_title} at {company} in {location}. \
        use the candidate resume below to extract his personal infos like firstname, lastname, adress, \
        phone number and email, outline his experience, education and skills. "
        #\n {candidate_resume}"
        chatgpt = ChatGPT("jobApp/secrets/openai.json")
        email_tosend = chatgpt.ask(query)
        job.applied = True
        return email_tosend
    

if __name__ == '__main__':
    pass