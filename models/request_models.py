# models/request_models.py
from pydantic import BaseModel

class PlatformCredRequest(BaseModel):
    _id: str
    _owner: str
    platform: str
    email: str
    password: str
    field_id: str
    created_date : str 
    
class JobSearchRequest(BaseModel):
    _id: str
    _owner: str
    platform: str
    job: str
    location: str
    field_id: str
    created_date : str 

class ApplyRequest(BaseModel):
    _id: str
    _owner: str
    platform: str
    job: str
    location: str
    firstname: str
    lastname: str 
    resume: str
    phone: str
    limit: str
    field_id: str
    created_date : str 
