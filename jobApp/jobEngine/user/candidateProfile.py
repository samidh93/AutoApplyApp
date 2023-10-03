from ..resume.resumeParser import Resume
from ..ai.chatgpt import ChatGPT
import json
from deprecated import deprecated
import phonenumbers
from phonenumbers import geocoder

"""
Candidate profile, Experiences, Educations, Skills
"""

class CandidateProfile:
    def __init__(self, resume_path, firstname, lastname, address, email, phone_number, limit, years_experience, desired_salary, visa_required,  educations:dict={}, experiences:dict={}, skills:dict={} , **more):
        self.resume = Resume(file_path=resume_path, candidate_firstname=firstname, candidate_lastname=lastname).resume
        #self.cv_nlp = ChatGPT("jobApp/secrets/openai.json")
        self.experiences = Experiences(experiences=experiences) 
        self.educations = Educations(educations=educations)
        self.skills = Skills(skills=skills)
        # access languages
        self.languages:list = self.skills.languages.languages
        self.experiences:list = self.skills.softwares.softwares
        self.years_experience = years_experience
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email
        self.phone_number = phone_number
        self.country_code,self.country_name = PhoneCodeExtractor.extract_country_code_name(self.phone_number)
        self.phone_code = "Germany (+49)"
        self.applications_limit = limit
        self.visa_required = visa_required
        self.desired_salary = desired_salary
        self.summary = None # will be generated automaticly with each job

    def generate_summary_for_job(self, job_title, company, platform, hiring_manager):
        self.summary =  f"Dear {hiring_manager or 'Hiring Manager'},\n\n\ \
            I am writing to express my keen interest in the {job_title} position at {company},\
            as advertised on {platform}. With a deep passion for my work and an extensive record of achievements, \
            I am enthusiastic about the opportunity to contribute my skills and drive to your dynamic team. \
            I am eager to meet with you in person or online to discuss how my qualifications align with your needs.\n\n\
            Sincerely,\n\
            {self.firstname} {self.lastname}"

        
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



class IT:
    def __init__(self, what:str, level:str): # what= office, level=good, what c++, level=advanced
        self.what_it = what
        self.it_level = level
class Language:
    def __init__(self, what, level):# what= en, level=good
        self.what_lang = what
        self.lang_level = level
class Languages: 
    def __init__(self, languages:dict) -> None:
        # Your code to process the dictionary goes here
        self.languages:[Language] = []
        for key, value in languages.items():
            print(f"Key: {key}, Value: {value}")
            self.languages.append(Language(key, value))

    def get_level(self, what_lang):
        for lang in self.languages:
            if what_lang ==lang.what:
                return lang.level
        return None

class Softwares:
    def __init__(self, softwares:dict) -> None:
        # Your code to process the dictionary goes here
        self.softwares = []
        for key, value in softwares.items():
            print(f"Key: {key}, Value: {value}")
            self.softwares.append(Language(key, value))
    def get_level(self, what_it):
        for soft in self.softwares:
            if what_it ==soft.what:
                return soft.level
        return None
# {"skills": 
#   {"Languages":
#           { 
#           "english": "good",
#            "german": "basic"
#            }
#   },
#   {"Softwares":
#            {
#           "ms_word": "good",
#            "powerpoint": "basic",
#            "sql": "good"
#             }
#    }
# }
class Skills:
    def __init__(self, skills:dict): 
        # Your code to process the dictionary goes here
        for key, value in skills.items():
            print(f"Key: {key}, Value: {value}")
            if key=="Languages": # pass the value down to the class
                self.languages = Languages(value)
            elif key == "Softwares":
                self.softwares = Softwares(value)

# Should be filled on the specific platform

class Experience:
    def __init__(self, job_title, company, duration):
        self.job_title = job_title
        self.company_name = company
        self.duration = duration

# {"experiences": 
#   {
#           "job_title": "engineer",
#            "company": "google",
#           "duration": "2 years"
#   }, etc
# }
class Experiences:
    def __init__(self, experiences:[dict]) -> None:
        self.experiences = []
        for exp in experiences:
            self.experiences.append(Experience(exp["job_title"], exp["company"], exp["duration"]))
class Education:
    def __init__(self, university, degree, duration):
        self.university = university
        self.degree = degree
        self.duration = duration

# {"educations": 
#   {
#           "university": "tu",
#            "degree": "master",
#           "duration": "2 years"
#   }, etc
# }
class Educations:
    def __init__(self, educations:[dict]) -> None:
        self.educations = []
        for educ in educations:
            self.educations.append(Experience(educ["university"], educ["degree"],educ["duration"]))


class PhoneCodeExtractor:
    @staticmethod
    def extract_country_code_name( mobile_number):
        try:
            # Parse the phone number
            phone_number = phonenumbers.parse(mobile_number, None)
            # Extract country code
            country_code = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            # Get country name
            country_name = geocoder.description_for_number(phone_number, "en")
            return country_code, country_name
        except phonenumbers.phonenumberutil.NumberParseException:
            return None, "Invalid phone number"
        except Exception as e:
            return None, str(e)

if __name__ == "__main__":
    candidate = CandidateProfile('jobApp/data/zayneb_dhieb_resume_english.pdf')
    candidate.extract_education_from_resume()
    candidate.extract_experience_from_resume()
    candidate.extract_personal_infos_from_resume()