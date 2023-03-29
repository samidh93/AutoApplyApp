from resumeParser import Resume
from chatgpt import ChatGPT
import json
import requests
from typing import List
import threading

class Experience:
    def __init__(self, job_title, company, duration):
        self.job_title = job_title
        self.company_name = company
        self.duration = duration
        
class Education:
    def __init__(self, institute, degree, duration):
        self.institute = institute
        self.degree = degree
        self.duration = duration
        
class Skills:
    def __init__(self, software, languages):
        self.languages = languages
        self.software = software

class CandidateProfile:
    def __init__(self, resume_path):
        
        self.resume = Resume(resume_path)
        self.resume_text = self.resume.extract_text()
        self.cv_nlp = ChatGPT("jobApp/secrets/openai.json")
        self.experience_list = []
        self.education_list = []
        self.skills_list = []

    def extract_candidate_data_from_resume(self): #all in one call, maybe difficult to get
        #request = "return experience, education and skills from the following resume: \n"
        pass
    def extract_candidate_personal_infos(self):
        pass

    def extract_experience(self)->list: # extract experience 
        request = "given the following resume, under experience, extract data like job_title, company_name and duration and return only these data as json. ignore unrelevant data\n"
        full_qs = request + self.resume_text
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        experience_data = json.loads(reply)
        for exp in experience_data:
            experience_obj = Experience(exp['job_title'], exp['company_name'], exp['duration'])
            print(experience_obj.company_name, experience_obj.job_title, experience_obj.duration)
            self.experience_list.append(experience_obj)
        return self.experience_list
    
    def extract_education(self)->list:
        request = "given the following resume, under education, extract data like institute, degree and duration or graduation date and return only these data as json. ignore unrelevant data\n"
        full_qs = request + self.resume_text
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        education_data = json.loads(reply)
        for edu in education_data:
            education_obj = Education(edu['institute'], edu['degree'], edu['duration'])
            print(education_obj.degree, education_obj.institute, education_obj.duration)
            self.education_list.append(education_obj)
        return self.education_list     
    def extract_skills(self)->list:
        request = "given the following resume, under skills, extract data like Software and Languages and return only these data as json. ignore unrelevant data\n"
        full_qs = request + self.resume_text
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        skills_data = json.loads(reply)
        for skill in skills_data:
            skills_obj = Skills(skill['Software'], skill['Languages'])
            print(skills_obj.software, skills_obj.languages)
            self.skills_list.append(skills_obj)
        return self.skills_list

if __name__ == "__main__":
    candidate = CandidateProfile('jobApp/data/zayneb_dhieb_resume_english.pdf')
    # Create worker threads
    t1 = threading.Thread(target=candidate.extract_experience, name="experience thread")
    t2 = threading.Thread(target=candidate.extract_education, name="education thread")
    t3 = threading.Thread(target=candidate.extract_skills, name="skills thread")

    # Start worker threads
    t1.start()
    t2.start()
    t3.start()
    # Wait for worker threads to finish
    t1.join()
    t2.join()
    t3.join()
