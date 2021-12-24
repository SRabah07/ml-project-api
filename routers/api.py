import logging
from fastapi import APIRouter, HTTPException
from password_validator import PasswordValidator
from starlette.status import HTTP_400_BAD_REQUEST
from models import MakePrediction, PredictionResult
from db.manage_model import get, get_all, get_by_version
from routers.predict import make_predict

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/models")
async def list_models():
    logger.info("Get models.")
    return await get_all()


@router.get("/models/{identifier:int}")
async def get_one(identifier: int):
    logger.info(f"Get model for identifier={identifier}")
    return await get(identifier)


@router.get("/models/{version:str}")
async def get_one_by_version(version: str):
    logger.info(f"Get model for version={version}")
    return await get_by_version(version)


@router.put('/predict')
async def prediction(info: MakePrediction):
    logger.info(f"Make prediction for {info}")
    model = None
    if info.version:
        model = await get_by_version(info.version)
    elif info.id > 0:
        model = await get(info.id)

    if not model:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="No model selected, a version's or identifier's model must be provided")

    rating = make_predict(model.key, info.text)
    return PredictionResult(model=model, rating=rating)
