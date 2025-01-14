# api/job_search.py
from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from models.request_models import ApplyRequest
from models.response_models import ApplyResponse
import time
from appCore import appCreatorLinkedin, LoginException
import logging


class JobApplyApi:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/api/job/apply/", self.apply, methods=["POST"])
        self.router.add_api_route(
            "/api/job/apply/jobs_applied/", self.get_applied_jobs, methods=["GET"])

    async def apply(self, jobs: ApplyRequest):
        try:
            applyReq = jobs.model_dump_json()
            logging.info(f"request job: {applyReq}")
            jobsQueryApp = appCreatorLinkedin(applyReq)
            # use threaded context
            logging.info(" applying for jobs")
            jobCount, jobList = jobsQueryApp.applyJobs()
            logging.info(f"jobs to apply for {jobCount}")
            if jobCount > 0:
                return ApplyResponse(
                    message=f"jobs apply service submitted successfully. applying for {jobCount} jobs",
                    data={"job_count": jobCount, "job_list":jobList ,"_owner": jobs.user.owner,"_id":jobs.field_id},
                    status="ok"
                )
            else:
                return ApplyResponse(
                    message=f"jobs apply service returned {jobCount} jobs",
                    data={"job_count": jobCount, "_owner": jobs.user.owner,"_id":jobs.field_id},
                    status="error"
                )
        except LoginException as loginError:
            logging.error("loginError occurred: %s", loginError)
            raise HTTPException(status_code=400, detail=str(loginError))
        except Exception as E:
            logging.error("Exception occurred: %s", E)
            raise HTTPException(status_code=500, detail=str(E))

    async def get_applied_jobs(self, unique_id: str) -> dict:
        try:
            logging.info(f"get jobs applied by unique id: {unique_id}")
            jobsQueryApp = appCreatorLinkedin()
            jobsCount, jobsDict = jobsQueryApp.getAppliedJobs(unique_id=unique_id)
            if isinstance(jobsDict, dict):
                logging.info(f"is valid dict : {jobsDict}")
            else: 
                logging.info(f"is not valid dict: {jobsDict}")

            if jobsCount > 0:
                logging.info(f"jobs applied for {jobsCount}")
                return {
                    "message":f"jobs completed: {jobsCount}",
                    "data":{"jobs": jobsDict},
                    "status":"ok"
                }                
            else:
                return {
                    "message":f"jobs completed: {jobsCount}",
                    "data":{"jobs": jobsDict},
                    "status":"error"
                }        
        except LoginException as loginError:
            logging.error("loginError occurred: %s", loginError)
            raise HTTPException(status_code=400, detail=str(loginError))
        except Exception as E:
            logging.error("Exception occurred: %s", E)
            raise HTTPException(status_code=500, detail=str(E))
