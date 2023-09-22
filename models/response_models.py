from pydantic import BaseModel

class JobCountResponse(BaseModel):
    message: str
    data: dict
    status: str