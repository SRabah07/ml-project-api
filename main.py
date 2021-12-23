from fastapi import Depends, FastAPI

import logging
import api_logging

import auth
import models
import routers
from db.init import init
from db.db import get_database
from dependencies import read_current_user

app = FastAPI()

app.include_router(routers.api.router, prefix="/api", tags=["API"], dependencies=[Depends(read_current_user)])
app.include_router(routers.register.router, prefix="/register", tags=["Register"])


@app.get("/")
async def home():
    return {"message": "Project 2: ML Sentiment Analysis API"}


@app.on_event("startup")
async def startup():
    logging.info('Startup Application...')
    await init()


@app.on_event("shutdown")
async def shutdown():
    logging.info('Shutdown Application...')
    await get_database().disconnect()
