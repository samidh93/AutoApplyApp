# api/__init__.py
from fastapi import APIRouter
from .job_search import JobSearchApi
from .linkedin_cred import LinkedinCredApi
from .job_apply import JobApplyApi

# define all api classes

jobSearchObj = JobSearchApi()
jobApplyApiObj  = JobApplyApi()
linkedinCredObj = LinkedinCredApi()

# define the routers
router = APIRouter()
router.include_router(jobSearchObj.router)
router.include_router(linkedinCredObj.router)
router.include_router(jobApplyApiObj.router)