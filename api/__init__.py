# api/__init__.py
from fastapi import APIRouter
from .job_search import router as job_search_router
from .test_linkedin_cred import router as test_linkedin_router

router = APIRouter()

router.include_router(job_search_router)
router.include_router( test_linkedin_router)