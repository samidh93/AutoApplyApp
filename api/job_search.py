# api/job_search.py
from fastapi import APIRouter, HTTPException
from models.request_models import JobSearchRequest
from models.response_models import JobSearchResponse
from appCore import appCreatorLinkedin, LoginException
import logging

router = APIRouter()

@router.post("/api/getJobCount/")
def get_job_count(jobs: JobSearchRequest):
    try:
        logging.info(f"request body: {jobs}")
        jobs_query = {
            "user":{
                "email": jobs.model_dump().get("email"),
                "password": jobs.model_dump().get("password"),
                "_owner": jobs.model_dump().get("_owner"),
                "field_id": jobs.model_dump().get("field_id"),
                "created_date": jobs.model_dump().get("created_date"),
            },
            "search_params": {
                "job": jobs.job,
                "location": jobs.location
            }
        }
        jobsQueryApp = appCreatorLinkedin(jobs_query)
        # use threaded context 
        jobCount = jobsQueryApp.collectJobs()
        logging.info(f"jobs count {jobCount}")
        if jobCount != 0:
            return JobSearchResponse(
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