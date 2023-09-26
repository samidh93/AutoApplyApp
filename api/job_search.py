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
        # use threaded context 
        jobCount = 430#jobsQueryApp.collectJobs()
        if jobCount != 0:
            return JobCountResponse(
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