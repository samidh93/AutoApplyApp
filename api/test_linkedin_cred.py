# api/job_search.py
from fastapi import APIRouter, HTTPException
from models.request_models import PlatformCredRequest
from appCore import appCreatorLinkedin, LoginException
from models.response_models import PlatformCredResponse
import logging

router = APIRouter()


@router.post("/api/testPlatformCredRequest/")
def testPlatformCredRequest(userCred: PlatformCredRequest):
    try:
        linkedinLoginData = {
            "user":{
                "email":userCred.model_dump().get("email"),
                "password":userCred.model_dump().get("password")
            }
        }
        PlatformCredRequestApp = appCreatorLinkedin(linkedinLoginData)
        PlatformCredRequestApp.tryCredentialsLinkedin()
        return PlatformCredResponse(
                message="Users Credentials verified successfully",
                data={"data": userCred.model_dump()}, 
                status="ok"
            )
        #raise CustomException("login failed")
    except LoginException as loginError:
        logging.error("loginError occurred: %s", loginError)
        raise HTTPException(status_code=400, detail=str(loginError))
    except Exception as E:
        logging.error("Exception occured: %s", E)
        raise HTTPException(status_code=500, detail=str(E))
