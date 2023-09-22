# main.py
from fastapi import FastAPI
from api import router as api_router
import logging_config  # Import the logging configuration

app = FastAPI(debug=True)

app.include_router(api_router)