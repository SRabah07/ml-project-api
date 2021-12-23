from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    admin: bool = False


class User(UserCreate):
    id: int
