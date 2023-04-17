from emailApplicationBuilder import EmailApplicationBuilder
from easyApplicationBuilder import EasyApplyApplicationBuilder
from directApplicationBuilder import DirectApplicationBuilder


class ApplicationDirector:
    def __init__(self):
        self.builder = None

    def construct_application(self, candidate_profile, jobs, application_type= 'Email' or 'Easy Apply' or 'Direct'):
        if application_type == 'Email':
            self.builder = EmailApplicationBuilder()
        elif application_type == 'Easy Apply':
            self.builder = EasyApplyApplicationBuilder()
        elif application_type == 'Direct':
            self.builder = DirectApplicationBuilder()
        else:
            raise ValueError('Invalid application type')

        self.builder.set_candidate_profile(candidate_profile)
        self.builder.set_jobs(jobs)

        return self.builder.build_application()



if __name__ == '__main__':
    from job import Job
    from jobBuilderLinkedin import JobBuilder, JobParser
    from emailCompanyBuilder import EmailCompanyBuilder
    from candidateProfile import CandidateProfile

    jobParserObj= JobParser('jobApp/secrets/linkedin.json')
    jobParserObj.setEasyApplyFilter(False) # optional as unauthenticated has no access to easy apply 
    jobLinks = jobParserObj.generateLinksPerPage(1)
    jobber = JobBuilder(jobLinks, "offSite" ) # can be upgraeded as a set( links, application_type)
    jobObjList = jobber.createJobObjectList()
    emailBuilder = EmailCompanyBuilder(jobObjList)    
    emailBuilder.buildEmailList() # generate company email
    candidate = CandidateProfile(resume_path='jobApp/data/zayneb_dhieb_resume_english.pdf', firstname="zayneb", lastname="dhieb", email="dhiebzayneb89@gmail.com", phone_number=+21620094923)
    appDirector = ApplicationDirector()
    emailapp= appDirector.construct_application(candidate_profile=candidate, jobs=jobObjList, application_type='Email')
    emailapp.ApplyForAll()
    
    #Resume.saveContentToDocx(emailDarft, 'jobApp/data/zayneb_dhieb_resume_english.docx')
    #jobber.storeAsCsv('jobApp/data/jobsOffSite.csv')
