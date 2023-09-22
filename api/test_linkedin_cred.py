# api/job_search.py
from fastapi import APIRouter, HTTPException
from models.request_models import LinkedinCred
from appCore import appCreatorLinkedin, LoginException
import logging

router = APIRouter()


@router.post("/api/testLinkedinCred/")
def testLinkedinCred(userCred: LinkedinCred):
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
    except Exception as E:
        logging.error("Exception occured: %s", E)
        raise HTTPException(status_code=500, detail=str(E))
