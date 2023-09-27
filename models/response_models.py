from pydantic import BaseModel

class PlatformCredResponse(BaseModel):
    message: str
    data: dict
    status: str

class JobSearchResponse(BaseModel):
    message: str
    data: dict
    status: str

class ApplyResponse(BaseModel):
    message: str
    data: dict
    status: str