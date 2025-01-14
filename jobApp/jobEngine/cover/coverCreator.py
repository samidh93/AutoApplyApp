import json

class CoverCreator:
    def __init__(self, cover_template:str = 'jobApp/data/cover.json', candidate=object, candidate_infos:list=None):
        self.cover_file = cover_template
        self.candidate = candidate
        self.candidate_infos = candidate_infos
        
    def __call__(self):
        if self.candidate_infos != None:
            return self.format_cover_template(self.candidate_infos)
        if self.candidate != None:
            return self.format_cover_template(self.candidate)
    
    def format_cover_template(self, list_vars):
        with open(self.cover_file, 'r') as f:
            return f.read().format(job_title=list_vars[0],
                                          company=list_vars[1],
                                          fullname=list_vars[2],
                                          phone_number=list_vars[3],)
        

if __name__ == '__main__':
    data = ["project manager", "stroomrecruitment", "name last", "number" ]
    formatted = CoverCreator(candidate_infos=data)()
    print(formatted)