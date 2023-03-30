from gmail import Gmail
from candidateProfile import CandidateProfile, ChatGPT
from jobBuilderLinkedin import JobBuilder, JobParser, Job


class ApplicationBuilder:
    def __init__(self, candidate: CandidateProfile, jobOffers:list[Job]) -> None:
        self.candidate = candidate
        self.jobs_to_apply_for = jobOffers

    def apply(self, job:Job):
        print(f"sending email application for {job.job_title} at {job.company_name} in {job.job_location}")
        gmail = Gmail('jobApp/secrets/credentials.json', 'jobApp/secrets/token.json' )
        gmail.send_email_with_attachments('dhiebzayneb89@gmail.com', f'job application as {job.job_title} at {job.company_name} in {job.job_location}', self.generateApplicationEmail(job), [self.candidate.resume.file_path])

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

    def applyAll(self):
        for job in self.jobs_to_apply_for:
            self.apply(job)

if __name__ == '__main__':
    # TODO: add json parser
    candidate = CandidateProfile('jobApp/data/zayneb_dhieb_resume_english.pdf')
    jobParserObj = JobParser(job_title="recruiting", location="France")
    jobs = jobParserObj.generateLinksPerPage(1)
    jobber = JobBuilder(jobs)
    joboffers = jobber.createJobObjectList()
    appBuild = ApplicationBuilder(candidate, joboffers)
    appBuild.applyAll()