# api/job_search.py
from fastapi import APIRouter, HTTPException
from models.request_models import JobSearchRequest
from models.response_models import JobSearchResponse
from appCore import appCreatorLinkedin, LoginException
import logging

class JobSearchApi:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/api/job/search/", self.search, methods=["POST"])
        self.router.add_api_route(
            "/api/job/search/jobs_found", self.get_found_jobs, methods=["GET"])
        self.router.add_api_route(
            "/api/job/search/jobs_searched", self.get_searched_jobs, methods=["GET"])

    async def search(self, jobs: JobSearchRequest):
        try:
            applyReq = jobs.model_dump_json()
            logging.info(f"request job: {applyReq}")
            jobsQueryApp = appCreatorLinkedin(applyReq)
            # use threaded context
            jobCount, jobLinks = jobsQueryApp.searchJobs()
            jobSearched = len(jobLinks)
            logging.info(f"jobs searched count {jobSearched}")
            if jobCount > 0:
                return JobSearchResponse(
                    message="jobs search service returned successfully",
                    # Wrap the jobCount in a dictionary
                    data={"job_count": jobCount,"job_searched":jobSearched ,"job_list": jobLinks, "_owner": jobs.user.owner,"_id":jobs.field_id},
                    status="ok"
                )
            else:
                return JobSearchResponse(
                    message="jobs search service returned no jobs",
                    # Wrap the jobCount in a dictionary
                    data={"job_count": jobCount , "_owner": jobs.user.owner,"_id":jobs.field_id},
                    status="error"
                )
        except LoginException as loginError:
            logging.error("loginError occurred: %s", loginError)
            raise HTTPException(status_code=400, detail=str(loginError))
        except Exception as E:
            logging.error("Exception occurred: %s", E)
            raise HTTPException(status_code=500, detail=str(E))

    async def get_found_jobs(self, jobs: JobSearchRequest) -> dict:
        try:
            applyReq = jobs.model_dump_json()
            logging.info(f"request job: {applyReq}")

            jobsQueryApp = appCreatorLinkedin(applyReq)
            jobCount = jobsQueryApp.getFoundJobs()
            logging.info(f"jobs count {jobCount}")
            if jobCount > 0:
                 return {
                    "message":"jobs collect service returned successfully",
                    # Wrap the jobCount in a dictionary
                    "data":{"job_count": jobCount, "_owner": jobs.user.owner,"_id":jobs.field_id},
                    "status":"ok"
                }
            else:
                return {
                    "message":"jobs collect service returned no jobs",
                    # Wrap the jobCount in a dictionary
                    "data":{"job_count": jobCount, "_owner": jobs.user.owner,"_id":jobs.field_id},
                    "status":"error"
                }
        except LoginException as loginError:
            logging.error("loginError occurred: %s", loginError)
            raise HTTPException(status_code=400, detail=str(loginError))
        except Exception as E:
            logging.error("Exception occurred: %s", E)
            raise HTTPException(status_code=500, detail=str(E))

    async def get_searched_jobs(self, unique_id: str) -> dict:
        try:
            logging.info(f"get jobs searched by unique id: {unique_id}")
            jobsQueryApp = appCreatorLinkedin()
            jobsCount, jobsDict = jobsQueryApp.getFoundJobs(
                unique_id=unique_id)
            if jobsCount > 0:
                logging.info(f"jobs searched for {jobsCount}")
                return JobSearchResponse(
                    message=f"jobs searched: {jobsCount}",
                    # Wrap the len(jobsDict) in a dictionary
                    data={"jobs": jobsDict},
                    status="ok"
                )
            else:
                return JobSearchResponse(
                    message=f"jobs searched: {jobsCount}",
                    # Wrap the len(jobsDict) in a dictionary
                    data={"jobs": jobsDict},
                    status="error"
                )
        except LoginException as loginError:
            logging.error("loginError occurred: %s", loginError)
            raise HTTPException(status_code=400, detail=str(loginError))
        except Exception as E:
            logging.error("Exception occurred: %s", E)
            raise HTTPException(status_code=500, detail=str(E))
