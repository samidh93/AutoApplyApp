# generate custom resume based on job description.
# needs: candidate_resume, job_description

from chatgpt import ChatGPT
from jobBuilderLinkedin import JobBuilder,JobParser, Job
from resumeParser import Resume, canvas

class ResumeBuilder:
    def __init__(self, resume_path, job=None):
        self.old_resume_content = Resume(resume_path).extract_text()
    
    def generateCustomResumeAi(self, job:Job) ->str:
        self.job_description = job.job_description
        self.chatgpt = ChatGPT("jobApp/secrets/openai.json")
        query = f"rewrite my resume by adding the required skills from the following job desciption. do not change the resume format and template.\n \
        Here is my resume: {self.old_resume_content}.\n Here is the job description: {self.job_description}."
        new_resume = self.chatgpt.ask(query)
        print(new_resume)
        return new_resume
    
    def createCustomResumePdf(self, job:Job, new_resume_path=None) -> None:
        """ create an ai customized resume and save it as pdf
            if new path is left blank,  write to jobApp/data/cv_name_last_jobTitle_comapny.pdf
        """
    #@TODO add applicant class
        name = "zayneb"
        last = "dhieb"
        if new_resume_path == None:
            new_resume_path = f"jobApp/data/cv_{name}_{last}_{job.job_title}_{job.company_name}.txt"
        with open(new_resume_path, "w") as f:
            f.write(self.generateCustomResumeAi(job))
        #Resume.saveContentToPdf(self.generateCustomResumeAi(job), new_resume_path)


if __name__ == '__main__':
    # TODO: add json parser
    jobParserObj = JobParser(job_title="recruiting", location="France")
    links = jobParserObj.generateLinksPerPage(1)
    jobObjs = JobBuilder(links)
    jobs= jobObjs.createJobObjectList()
    CvCustomizer = ResumeBuilder(
            'jobApp/data/zayneb_dhieb_resume_english.pdf')
    for job in jobs:
        #customCv = CvCustomizer.generateCustomResumeAi(job)
        CvCustomizer.createCustomResumePdf(job)
        break
