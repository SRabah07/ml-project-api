from pydantic import BaseModel
from typing import Optional, Any


class UserCreate(BaseModel):
    username: str
    password: str
    admin: bool = False


class User(UserCreate):
    id: int


class Metrics(BaseModel):
    accuracy: Optional[float] = None,
    recall: Optional[float] = None,
    precision: Optional[float] = None,
    f1: Optional[float] = None,
    fbeta: Optional[float] = None,


class Model(BaseModel):
    id: int
    key: str
    version: str
    type: str
    model: str
    branch: str
    description: str
    metrics: Any

class MakePrediction(BaseModel):
    id: Optional[int]
    version: Optional[str]
    text: str


class SentimentPredictionResult(BaseModel):
    model: Model
    rating: int


class StrokeObservation(BaseModel):
    gender: str
    age: float
    hypertension: str
    heart_disease: str
    Residence_type: str
    avg_glucose_level: float
    bmi: Optional[float] = None
    smoking_status: str


class StrokePredictionRequest(BaseModel):
    observation: StrokeObservation
    id: Optional[int]
    version: Optional[str]


class StrokePredictionResult(BaseModel):
    observation: StrokeObservation
    prediction: str
