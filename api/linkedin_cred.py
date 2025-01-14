# api/job_search.py
from fastapi import APIRouter, HTTPException
from models.request_models import PlatformCredRequest
from appCore import appCreatorLinkedin, LoginException
from models.response_models import PlatformCredResponse
import logging

class LinkedinCredApi:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/api/platform/linkedin/verify/", self.verify, methods=["POST"])
        self.router.add_api_route("/api/platform/linkedin/cookies", self.get_cookies, methods=["GET"])
        
    async def verify(self, userCred: PlatformCredRequest):
        try:
            #logging.info(f"owner_id: {userCred.user.owner}")
            applyReq = userCred.model_dump_json()
            logging.info(f"applyreq: {applyReq}")

            PlatformCredRequestApp = appCreatorLinkedin(applyReq)
            verified, cookies = PlatformCredRequestApp.tryCredentialsLinkedin()
            if verified:
                return PlatformCredResponse(
                        message="Users Credentials verified successfully",
                        data={"_owner": userCred.user.owner,"_id":userCred.user.field_id, "verified": verified, "cookies": cookies}, 
                        status="ok"
                    )
            else:
                return PlatformCredResponse(
                        message="Users Credentials could not be verified",
                        data={"_owner": userCred.user.owner,"_id":userCred.user.field_id, "verified": verified, "cookies": cookies}, 
                        status="error"
                    )   
            #raise CustomException("login failed")
        except LoginException as loginError:
            logging.error("loginError occurred: %s", str(loginError))
            raise HTTPException(status_code=400, detail=str(loginError))
        except Exception as E:
            logging.error("Exception occured: %s", str(E))
            raise HTTPException(status_code=500, detail=str(E))
        
    async def get_cookies(self, unique_id:str)->PlatformCredResponse:
        try:
            logging.info(f"get cookies found by unique id: {unique_id}")
            PlatformCredRequestApp = appCreatorLinkedin()
            cookies  = PlatformCredRequestApp.getCookiesLinkedin(unique_id=unique_id)
            if cookies != None:
                logging.info(f"cookies found for linkedin user")
                return PlatformCredResponse(
                    message=f"cookies found",
                    data={"cookies": cookies},  # Wrap the len(jobsDict) in a dictionary
                    status="ok"
                )
            else:
                return PlatformCredResponse(
                    message=f"cookies not found",
                    data={"cookies": cookies},  # Wrap the len(jobsDict) in a dictionary
                    status="error"
                )
        except LoginException as loginError:
            logging.error("loginError occurred: %s", loginError)
            raise HTTPException(status_code=400, detail=str(loginError))
        except Exception as E:
            logging.error("Exception occurred: %s", E)
            raise HTTPException(status_code=500, detail=str(E))
