# models/request_models.py
from pydantic import BaseModel, Field
from typing import Optional

# by default all fields (also inherited) are mandatory, override them to optional in subclasses inf not mandatory
class PlatformCredRequest(BaseModel):
    _owner: str
    platform: str
    email: str
    password: str
    field_id: str
    created_date : str 
    
class JobSearchRequest(PlatformCredRequest):
    job: str
    location: str
    # MAke these optionals if the login session will be kept alive or credentials are saved locally after
   # email: Optional[str] = Field(None, title="Email", description="Optional") 
   # password: Optional[str] = Field(None, title="Password", description="Optional")

class ApplyRequest(JobSearchRequest):
    firstname: str
    lastname: str 
    resume: str
    phone: str
    limit: str
    # MAke these optionals if the login session will be kept alive  or credentials are saved locally after
   # email: Optional[str] = Field(None, title="Email", description="Optional") 
   # password: Optional[str] = Field(None, title="Password", description="Optional")