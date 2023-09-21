from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from appCore import appCreatorLinkedin


app = FastAPI()
class linkedinCred(BaseModel):
    _id: str
    _owner: str
    title: str
    email: str
    password: str


@app.post("/api/testLinkedinCred/")
def testLinkedinCred(userCred: linkedinCred):
    try:
        linkedinLoginData = {
            "user":{
                "email":userCred.model_dump().get("email"),
                "password":userCred.model_dump().get("password")
            }
        }
        linkedinCredApp = appCreatorLinkedin(linkedinLoginData)
        loginSuccess = linkedinCredApp.tryCredentialsLinkedin()
        if loginSuccess:
            return {"message": "Users Credentials tested successfully", "data": userCred.model_dump(), "status": "ok"}
    except Exception as E:
            print("Exception occured: ", E)
            return {"message": "Users Credentials error", "data": userCred.model_dump(), "status": "!ok"}