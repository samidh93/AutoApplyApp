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
        applyReq = {
            "candidate": {
                "limit": job.limit,
            }
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