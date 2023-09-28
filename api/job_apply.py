# api/job_search.py
from fastapi import APIRouter, HTTPException
from models.request_models import ApplyRequest
from models.response_models import ApplyResponse

from appCore import appCreatorLinkedin, LoginException
import logging

router = APIRouter()

@router.post("/api/apply/")
def apply(job: ApplyRequest):
    try:
        logging.info(f"request body: {job}")
        applyReq = {
            "user":{
                "email": job.model_dump().get("email"),
                "password": job.model_dump().get("password"),
                "_owner": job.model_dump().get("_owner"),
                "field_id": job.model_dump().get("field_id"),
                "created_date": job.model_dump().get("created_date"),
            },
            "search_params": {
                "job": job.job,
                "location": job.location
            },
            "candidate":{
                "firstname": job.model_dump().get("firstname"),
                "lastname": job.model_dump().get("lastname"), 
                "resume": job.model_dump().get("resume"),
                "phone": job.model_dump().get("phone"),
                "limit": job.model_dump().get("limit"),
            }
            # extended with more params such salary and experience
        }
        jobsQueryApp = appCreatorLinkedin(applyReq)
        # use threaded context 
        jobCount = 430#jobsQueryApp.collectJobs()
        logging.info(f"jobs count {jobCount}")
        if jobCount != 0:
            return ApplyResponse(
                message="jobs count returned successfully",
                data={"job_count": jobCount},  # Wrap the jobCount in a dictionary
                status="ok"
            )
        else:
            raise HTTPException(status_code=400, detail="no jobs found")
    except LoginException as loginError:
        logging.error("loginError occurred: %s", loginError)
        raise HTTPException(status_code=400, detail=str(loginError))
    except Exception as E:
        logging.error("Exception occurred: %s", E)
        raise HTTPException(status_code=500, detail=str(E))