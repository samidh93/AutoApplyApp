# main.py
from fastapi import FastAPI
from api import router as api_router
import logging_config  # Import the logging configuration
import uvicorn

app = FastAPI(debug=True)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)