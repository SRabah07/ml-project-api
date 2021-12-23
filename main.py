from fastapi import Depends, FastAPI

import auth
import models
import routers
import dependencies

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Project 2: ML Sentiment Analysis API"}
