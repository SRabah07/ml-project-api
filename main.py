from fastapi import Depends, FastAPI, Request
import auth
import models
import routers
from db.init import init
from db.db import get_database
from dependencies import read_current_user
import os
import logging
import time
import traceback

LOGGING_CONFIG_FILE = os.environ.get('LOGGING_CONFIG_FILE', "logging.config")
LOGGING_FILE = os.environ.get('LOGGING_FILE', "api.log")

logging.config.fileConfig(LOGGING_CONFIG_FILE, defaults={"logging_file_name": LOGGING_FILE},
                          disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(routers.api.router, prefix="/api", tags=["API"], dependencies=[Depends(read_current_user)])
app.include_router(routers.register.router, prefix="/register", tags=["Register"])


@app.get("/")
async def home():
    return {"message": "Project 2: ML Sentiment Analysis API"}


@app.get("/readiness")
async def readiness():
    return {"status": "OK", "message": "Everything is up!"}


@app.on_event("startup")
async def startup():
    logger.info('Startup Application...')
    await init()


@app.on_event("shutdown")
async def shutdown():
    logger.info('Shutdown Application...')
    await get_database().disconnect()
