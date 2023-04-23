from applicationAbstract import Application
from candidateProfile import CandidateProfile, ChatGPT, Resume
from jobBuilderLinkedin import JobBuilder, JobParser, Job
from gmail import Gmail
import json
import os
from deprecated import deprecated
import csv

class EmailApplication(Application):
    def __init__(self, candidate_profile: CandidateProfile, jobs: list[Job], csvJobsFile='jobApp/data/jobs.csv'):
        self.candidate_profile = candidate_profile
        self.jobs = jobs
        self.type = 'Email'
        self.gmail_client = Gmail('jobApp/secrets/credentials_zayneb.json', 'jobApp/secrets/gmail_token.json' )
        self.candidate_experiences= self.candidate_profile.resume.extract_experience_section()
        self.candidate_educations= self.candidate_profile.resume.extract_education_section()
        self.candidate_infos= self.candidate_profile.resume.extract_info_section()
        super().__init__(candidate=candidate_profile, jobOffers=jobs ,csvJobsFile=csvJobsFile)
 


    def ApplyForJob(self, job: Job):
        status = False
        print(f"sending email application for {job.job_title} at {job.company_name} in {job.job_location}")
        #TODO: put threadpool if email is a list
        # as we have a list of possible emails
        if len(job.company_email) > 1:
            print("The email list has multiple elements:")
            for email in job.company_email:
                print(f"email to send: {email}")
                status = self.gmail_client.send_email_with_attachments(f'{self.candidate_profile.email}',f'{email}',  f'job application as {job.job_title} at {job.company_name} in {job.job_location}', self.generateApplicationTemplate(job), [self.candidate_profile.resume.file_path])
                if status:
                    job.setJobApplied(True) # applied for job
                    print(f"set job applied {job.applied}")
        elif len(job.company_email) == 1:
            print("The email list has only one element:")
            email = job.company_email[0]
            print(f"email to send: {email}")
            status = self.gmail_client.send_email_with_attachments(f'{self.candidate_profile.email}',f'{email}',  f'job application as {job.job_title} at {job.company_name} in {job.job_location}', self.generateApplicationTemplate(job), [self.candidate_profile.resume.file_path])
            if status:
                job.setJobApplied(True) # applied for job
                print(f"set job applied {job.applied}")
        else:
            print("The email list is empty")
    def ApplyForAll(self):
        return super().ApplyForAll()

    # generate application email specific for job: use ai to generate 
    @deprecated(reason="generate application email deprecated, use generateApplicationTemplate instead")
    def generateApplicationEmail(self, job:Job):
        query = f"create a job application email draft for the job {job.job_title} at {job.company_name} in {job.job_location} to the hiring manager. \
        use my personal infos: {self.candidate_infos} , experiences: {self.candidate_experiences} and educations: {self.candidate_educations} to highlight my worth\
        here is the job description to apply for: {job.job_description}. close the draft by leaving my contact details. ignore the adress and driving licence."
        chatgpt = ChatGPT("jobApp/secrets/openai.json")
        email_tosend = chatgpt.ask(query)
        return email_tosend
    
    # generate application email as a template for all: create one template with ai
    def generateApplicationTemplate(self, job:Job,  output_file:str='jobApp/data/email_draft_template.json')-> str:
        email_data = {
        "job_title": job.job_title,
        "company": job.company_name,
        "fullname": self.candidate_profile.firstname +" "+ self.candidate_profile.lastname,
        "phone_number": self.candidate_profile.phone_number
    }
        try:
            with open(output_file, "r") as f:
                template = f.read()
            #print(template.format(**email_data))
            return (template.format(**email_data))
        except FileNotFoundError:
            print("The file does not exist.")

        query = f"create a job application email draft as {'{job_title}'} at {'{company}'} to the hiring manager.\
        highlight the experiences: {self.candidate_experiences} and educations: {self.candidate_educations} \
        sincerely, {'{fullname}'} {'{phone_number}'}"
        chatgpt = ChatGPT("jobApp/secrets/openai.json")
        #print(f"query: {query}")
        template = chatgpt.ask(query)
        with open(output_file, "w") as f:
            json.dump(template, f)
        return template.format(**email_data)

if __name__ == '__main__':
    candidate = CandidateProfile(resume_path='jobApp/data/zayneb_dhieb_resume_english.pdf', firstname="zayneb", lastname="dhieb", email="samihomiebro@gmail.com", phone_number="+21620094923")
    jobs = [Job(1, None, "Human Resources Business Partner m/w/d", "precise hotels and resorts","Berlin", "one day ago", "as recruiting specialist you will help us achieve our goals", company_email=["jobs@begu.com"])]
    emailApply = EmailApplication(candidate, jobs)
    emailApply.ApplyForAll()