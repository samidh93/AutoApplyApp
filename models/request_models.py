# models/request_models.py
from pydantic import BaseModel, Field
from typing import Dict
from typing import Optional

# by default all fields (also inherited) are mandatory, override them to optional in subclasses inf not mandatory
class User(BaseModel):
    owner: str
    platform: str
    email: str
    password: str
    field_id: str
    created_date : str

class PlatformCredRequest(BaseModel):
    user:User

class SearchParams(BaseModel):
    job: str
    location: str
    limit: str

class JobSearchRequest(PlatformCredRequest):
    search_params:SearchParams
    field_id:str

class Address(BaseModel):
    street: str
    city: str
    plz: str
    country: str

class Experience(BaseModel):
    job_title: str
    company: str
    duration: str

class Education(BaseModel):
    university: str
    degree: str
    duration: str

class Skills(BaseModel):
    Languages: Dict[str, str]
    Softwares: Dict[str, str]

class Candidate(BaseModel):
    firstname: str
    lastname: str
    gender: str
    resume: str
    phone_number: str
    address: Address
    limit: str
    visa_required: str
    start_date: str
    years_experience: str
    desired_salary: str
    experiences: list[Experience]
    educations: list[Education]
    skills: Skills

class ApplyRequest(JobSearchRequest):
    candidate: Candidate
    field_id:str


