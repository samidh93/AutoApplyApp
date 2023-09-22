# api/job_search.py
from fastapi import APIRouter, HTTPException
from models.request_models import JobSearch
from models.response_models import JobCountResponse
from appCore import appCreatorLinkedin, LoginException
import logging

router = APIRouter()

@router.post("/api/getJobCount/")
def get_job_count(jobs: JobSearch):
    try:
        jobs_query = {
            "search_params": {
                "job": jobs.job,
                "location": jobs.location
            }
        }
        jobsQueryApp = appCreatorLinkedin(jobs_query)
        # jobsQueryApp.tryCredentialsLinkedin()
        return JobCountResponse(
            message="Users Credentials tested successfully",
            data=jobs_query,
            status="ok"
        )
    except LoginException as loginError:
        logging.error("loginError occurred: %s", loginError)
        raise HTTPException(status_code=400, detail=str(loginError))
    except Exception as E:
        logging.error("Exception occurred: %s", E)
        raise HTTPException(status_code=500, detail=str(E))