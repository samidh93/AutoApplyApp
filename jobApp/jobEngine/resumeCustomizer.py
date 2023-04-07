# generate custom resume based on job description.
# needs: candidate_resume, job_description

from chatgpt import ChatGPT
from jobBuilderLinkedin import JobBuilder,JobParser, Job
from resumeParser import Resume, canvas

class ResumeBuilder:
    def __init__(self, resume_path, job=None):
        self.old_resume_content = Resume(resume_path).extract_text()
        self.job_description = job.job_description

    
    def generateCustomResumeAi(self, job:Job) ->str:
        self.job_description = job.job_description
        self.chatgpt = ChatGPT("jobApp/secrets/openai.json")
        query = f"Rewrite my resume and tailor it to the job description below. \
        Here is my resume: {self.old_resume_content}. Here is the job description: {self.job_description}."
        new_resume = self.chatgpt.ask(query)
        print(new_resume)
        return new_resume
    
    def createCustomResumePdf(self, job:Job, new_resume_path:str) -> None:
        """ create an ai customized resume and save it as pdf
            if new path is left blank,  write to jobApp/data/cv_name_last_jobTitle_comapny.pdf
        """
    #@TODO add applicant class
        name = "alex"
        last = "red"
        if new_resume_path == None:
            new_resume_path = f"jobApp/data/cv_{name}_{last}_{job.job_title}_{job.company_name}.pdf"
        Resume.saveContentToPdf(self.generateCustomResumeAi(job), new_resume_path)


if __name__ == '__main__':
    # TODO: add json parser
    jobParserObj = JobParser(job_title="recruiting", location="France")
    links = jobParserObj.generateLinksPerPage(1)
    jobObjs = JobBuilder(links)
    jobs= jobObjs.createJobObjectList()
    CvCustomizer = ResumeBuilder(
            'jobApp/data/zayneb_dhieb_resume_english.pdf')
    for job in jobs:
        customCv = CvCustomizer.generateCustomResumeAi(
            'jobApp/data/zayneb_dhieb_resume_english.pdf', job)
