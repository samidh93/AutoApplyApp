# generate custom resume based on job description.
# needs: candidate_resume, job_description

from chatgpt import ChatGPT


class ResumeBuilder:
    def __init__(self, resume_path, job_description):
        self.old_resume = resume_path
        self.job_description = job_description
        chatai = ChatGPT("jobApp/secrets/openai.json")
        query = f"Rewrite my resume and tailor it to the job description below. \
        Here is my resume: {resume_path}. Here is the job description: {job_description}."
        new_resume = chatai.ask(query)
        return new_resume


if __name__ == '__main__':
    CvCustom = ResumeBuilder(
        'jobApp/data/zayneb_dhieb_resume_english.pdf', job_description)
