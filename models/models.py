from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    admin: bool = False


class User(UserCreate):
    id: int


class Model(BaseModel):
    id: int
    key: str
    version: str
    type: str
    branch: str
    description: str
    score: float


class MakePrediction(BaseModel):
    id: Optional[int]
    version: Optional[int]
    text: str


class PredictionResult(BaseModel):
    model: Model
    rating: int
