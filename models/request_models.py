# models/request_models.py
from pydantic import BaseModel

class LinkedinCred(BaseModel):
    _id: str
    _owner: str
    title: str
    email: str
    password: str

class JobSearch(BaseModel):
    _id: str
    _owner: str
    title: str
    job: str
    location: str
