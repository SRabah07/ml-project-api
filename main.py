from fastapi import Depends, FastAPI

import auth
import models
import routers
from dependencies import read_current_user

app = FastAPI()

app.include_router(routers.api.router, prefix="/api", tags=["API"], dependencies=[Depends(read_current_user)])
app.include_router(routers.register.router, prefix="/register", tags=["Register"])


@app.get("/")
async def home():
    return {"message": "Project 2: ML Sentiment Analysis API"}
