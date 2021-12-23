from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    admin: bool = False


class User(UserCreate):
    id: int
