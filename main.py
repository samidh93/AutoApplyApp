from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from appCore import appCreatorLinkedin, LoginException
import logging_config  # Import the logging configuration
import logging



app = FastAPI(debug=True)
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
        linkedinCredApp.tryCredentialsLinkedin()
        return {"message": "Users Credentials tested successfully", "data": userCred.model_dump(), "status": "ok"}
        #raise CustomException("login failed")
    except LoginException as loginError:
        logging.error("loginError occurred: %s", loginError)
        raise HTTPException(status_code=400, detail=str(loginError))
        return {"error": str(loginError), "data": userCred.model_dump(), "status": "err"}
    except Exception as E:
        logging.error("Exception occured: %s", E)
        raise HTTPException(status_code=500, detail=str(E))
        return {"error": str(E), "data": userCred.model_dump(), "status": "err"}