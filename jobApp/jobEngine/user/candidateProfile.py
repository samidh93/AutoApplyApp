from ..resume.resumeParser import Resume
from ..ai.chatgpt import ChatGPT
import json
from deprecated import deprecated

"""
    Candidate profile, Experiences, Educations, Skills
"""
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
    def __init__(self, softwares: list, languages:list):
        self.languages = languages
        self.softwares = softwares


## create more dynamic classes based on sections in resume 
class CandidateProfile:

    def __init__(self, resume_path, firstname=None, lastname=None, address=None, email=None, phone_number=None, linkedin=None):
        self.resume = Resume(resume_path)
        self.resume_text = self.resume.extract_text()
        self.cv_nlp = ChatGPT("jobApp/secrets/openai.json")
        self.experience_list = [Experience]
        self.education_list = [Education]
        self.skills_list = [Skills]
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.linkedin = linkedin
        self.phone_code = "Germany (+49)"

        # test cases
        self.set_expected_salary("50000")
        self.set_languages_expertise("C1")
        self.set_nationality("Tunisian")
        self.set_years_experiences("5")

    def set_nationality(self, nationality:str):
        self.nationality = nationality
    def set_expected_salary(self, salary:str):
        self.salary = salary
    def set_years_experiences(self, years:str):
        self.years_exp= years
    def set_languages_expertise(self, languages_expertise: str):
        self.languages_expert = languages_expertise
    def set_visa_requirement(self, job_location:str):
        if self.nationality == job_location:
            return False
        return True
    def extract_resume_plain_text(self):
        return self.resume_text


    def extract_personal_infos_from_resume(self): #all in one call, maybe difficult to get
        request = "given the following personal informations, return data as json like ['firstname': 'xxx', 'lastname': 'xxx', 'address': 'xxx', 'email': 'xxx', 'phone_number':'xxx', 'linkedin': 'xxx' ] if any data is missing return empty value. no header personal infos is required.\n"
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
    
       
    def extract_experience_from_resume(self)->list: # extract experience 
        request = "given the following experience, return these data as json like ['job_title': 'xxx', 'company_name': 'xxx' and 'duration': 'xxx'] no header experience is required.\n"
        full_qs = request + self.resume.extract_experience_section()
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        experience_data = json.loads(reply)
        for exp in experience_data:
            experience_obj = Experience(exp['job_title'], exp['company_name'], exp['duration'])
            print(experience_obj.company_name, experience_obj.job_title, experience_obj.duration)
            self.experience_list.append(experience_obj)
        return self.experience_list
    
    def extract_education_from_resume(self)->list:
        request = "given the following education, return these data as json like ['university': 'xxx', 'degree': 'xxx' and 'graduation_date': 'xxx'] no header education is required.\n"
        full_qs = request + self.resume.extract_education_section()
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        education_data = json.loads(reply)
        for edu in education_data:
            education_obj = Education(edu['university'], edu['degree'], edu['graduation_date'])
            print(education_obj.degree, education_obj.university, education_obj.duration)
            self.education_list.append(education_obj)
        return self.education_list     
    
    def extract_skills_from_resume(self)->list:
        request = "given the following skills, return these data as json like ['Software': '[xxx]' and 'Languages': '[xxx]'] no header skills is required.S\n"
        full_qs = request + self.resume.extract_skills_section()
        reply = self.cv_nlp.ask(full_qs)
        print(f"chatgpt replied\n {reply}")
        skills_data = json.loads(reply)
        skills_obj = Skills(skills_data['Software'], skills_data['Languages'])
        print(skills_obj.softwares, skills_obj.languages)
        self.skills_list.append(skills_obj)
        return self.skills_list

    ### @UPDATE: openai may not process the full resume due to 4095 tokens limit, using sections instead.
    @deprecated(reason="This method is no longer supported. Use extract sections methods instead.")
    def extract_all_from_resume(self):
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
 
if __name__ == "__main__":
    candidate = CandidateProfile('jobApp/data/zayneb_dhieb_resume_english.pdf')
    candidate.extract_education_from_resume()
    candidate.extract_experience_from_resume()
    candidate.extract_personal_infos_from_resume()