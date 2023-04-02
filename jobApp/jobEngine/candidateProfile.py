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
    def __init__(self, university, degree, duration):
        self.university = university
        self.degree = degree
        self.duration = duration
        
class Skills:
    def __init__(self, softwares, languages):
        self.languages = languages
        self.softwares = softwares

class CandidateProfile:

    def __init__(self, resume_path, firstname=None, lastname=None, address=None, email=None, phone_number=None, linkedin=None):
        self.resume = Resume(resume_path)
        self.resume_text = self.resume.extract_text()
        self.cv_nlp = ChatGPT("jobApp/secrets/openai.json")
        self.experience_list = []
        self.education_list = []
        self.skills_list = []
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.linkedin = linkedin
        
    def extract_resume_plain_text(self):
        return self.resume_text
    def extract_candidate_data_from_resume(self): #all in one call, maybe difficult to get
        request = "given the following resume, extract candidate information data and return only these data as json like ['firstname': 'xxx', 'lastname': 'xxx', 'address': 'xxx', 'email': 'xxx', 'phone_number':'xxx', 'linkedin': 'xxx' ] if any data is missing return empty value. no header personal infos is required. ignore unrelevant data\n \
        under education, extract data and return only these data as json like ['university': 'xxx', 'degree': 'xxx' and 'duration': 'xxx' or 'graduation_date': 'xxx'] no header education is required. ignore unrelevant data, max result are 3\n \
        under experience, extract data and return only these data as json like ['job_title': 'xxx', 'company_name': 'xxx' and 'duration': 'xxx'] no header experience is required. ignore unrelevant data\n \
        under skills, extract data and return only these data as json like ['Software': '[xxx]' and 'Languages': '[xxx]'] no header skills is required. ignore unrelevant data\n"
        full_qs = request + self.resume_text
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        infos_data = json.loads(reply)
        self.firstname = infos_data['firstname']
        self.lastname = infos_data['lastname']
        self.address = infos_data['address']
        self.email = infos_data['email']
        self.phone_number = infos_data['phone_number']
        self.linkedin = infos_data['linkedin']

    def extract_candidate_personal_infos(self):
        request = "given the following resume, extract candidate information data and return only these data as json like ['firstname': 'xxx', 'lastname': 'xxx', 'address': 'xxx', 'email': 'xxx', 'phone_number':'xxx', 'linkedin': 'xxx' ] if any data is missing return empty value. no header personal infos is required. ignore unrelevant data\n"
        full_qs = request + self.resume_text
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        infos_data = json.loads(reply)
        self.firstname = infos_data['firstname']
        self.lastname = infos_data['lastname']
        self.address = infos_data['address']
        self.email = infos_data['email']
        self.phone_number = infos_data['phone_number']
        self.linkedin = infos_data['linkedin']
        for exp in infos_data['experience']:
            experience_obj = Experience(exp['job_title'], exp['company_name'], exp['duration'])
            print(experience_obj.company_name, experience_obj.job_title, experience_obj.duration)
            self.experience_list.append(experience_obj)
        for edu in infos_data['education']:
            education_obj = Education(edu['university'], edu['degree'], edu['duration'] or edu['graduation_date'])
            print(education_obj.degree, education_obj.university, education_obj.duration)
            self.education_list.append(education_obj)
        skills_obj = Skills(infos_data['skills']['Software'], infos_data['skills']['Languages'])
        print(skills_obj.softwares, skills_obj.languages)
        
    def extract_experience(self)->list: # extract experience 
        request = "given the following resume, under experience, extract data and return only these data as json like ['job_title': 'xxx', 'company_name': 'xxx' and 'duration': 'xxx'] no header experience is required. ignore unrelevant data\n"
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
        request = "given the following resume, under education, extract data and return only these data as json like ['university': 'xxx', 'degree': 'xxx' and 'duration': 'xxx' or 'graduation_date': 'xxx'] no header education is required. ignore unrelevant data, max result are 3\n"
        full_qs = request + self.resume_text
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        education_data = json.loads(reply)
        for edu in education_data:
            education_obj = Education(edu['university'], edu['degree'], edu['duration'] or edu['graduation_date'])
            print(education_obj.degree, education_obj.university, education_obj.duration)
            self.education_list.append(education_obj)
        return self.education_list     
    
    def extract_skills(self)->list:
        request = "given the following resume, under skills, extract data and return only these data as json like ['Software': '[xxx]' and 'Languages': '[xxx]'] no header skills is required. ignore unrelevant data\n"
        full_qs = request + self.resume_text
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        skills_data = json.loads(reply)
        skills_obj = Skills(skills_data['Software'], skills_data['Languages'])
        print(skills_obj.softwares, skills_obj.languages)
        self.skills_list.append(skills_obj)
        return self.skills_list

if __name__ == "__main__":
    candidate = CandidateProfile('jobApp/data/zayneb_dhieb_resume_english.pdf')
    # Create worker threads
    t1 = threading.Thread(target=candidate.extract_candidate_data_from_resume, name="data thread")
    #t2 = threading.Thread(target=candidate.extract_education, name="education thread")
    #t3 = threading.Thread(target=candidate.extract_skills, name="skills thread")

    # Start worker threads
    t1.start()
    #t2.start()
    #t3.start()
    # Wait for worker threads to finish
    t1.join()
    #t2.join()
    #
    # t3.join()
