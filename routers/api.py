import logging
from fastapi import APIRouter, HTTPException
from password_validator import PasswordValidator
from starlette.status import HTTP_400_BAD_REQUEST
from models import MakePrediction, SentimentPredictionResult, StrokeObservation, StrokePredictionResult, \
    StrokePredictionRequest
from db.manage_model import get, get_all, get_by_version, get_by_type_and_version
from routers.predict_sentiment import make_sentiment_prediction
from routers.predict_stroke import make_stroke_prediction

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


@router.get("/models/{type:str}/{version:str}")
async def get_one_by_version(type: str, version: str):
    logger.info(f"Get model of type={type}, version={version}")
    return await get_by_type_and_version(type, version)


@router.put('/predict/sentiment')
async def predict_sentiment(info: MakePrediction) -> SentimentPredictionResult:
    logger.info(f"Make prediction type of Sentiment, for data= {info}")
    model = None
    if info.version:
        model = await get_by_type_and_version("Sentiment", info.version)
    elif info.id and info.id > 0:
        model = await get(info.id)

    if not model:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="No model selected, a version's or identifier's model must be provided")

    rating = make_sentiment_prediction(model.key, info.text)
    return SentimentPredictionResult(model=model, rating=rating)


@router.put('/predict/stroke')
async def predict_stroke(prediction_request: StrokePredictionRequest) -> StrokePredictionResult:
    logger.info(f"Make prediction type of Stroke, for observation= {prediction_request}")
    model = None
    if prediction_request.version:
        model = await get_by_type_and_version("Stroke", prediction_request.version)
    elif prediction_request.id and prediction_request.id > 0:
        model = await get(prediction_request.id)

    if not model:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="No model selected, a version's or identifier's model must be provided")

    prediction = make_stroke_prediction(model.key, prediction_request.observation)
    return StrokePredictionResult(observation=prediction_request.observation, prediction=prediction)
