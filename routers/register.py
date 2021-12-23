from fastapi import APIRouter, HTTPException
from password_validator import PasswordValidator
from starlette.status import HTTP_400_BAD_REQUEST
from models import UserCreate

router = APIRouter()

MIN_CHARACTERS_USERNAME = 5

# Password validator
schema = PasswordValidator()
schema \
    .min(8) \
    .max(15) \
    .has().uppercase() \
    .has().lowercase() \
    .has().digits() \
    .has().no().spaces()


@router.post('/')
def register(user: UserCreate):
    validate(user)


def validate(user: UserCreate):
    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User is required!")

    # Login / Username
    if len(user.username < MIN_CHARACTERS_USERNAME):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="Username/Login must be at least {MIN_CHARACTERS_USERNAME} characters")

    # Password
    if not schema.validate(user.password):
        detail = """
        Password must be:
        - At least 8 characters
        - At least one uppercase
        - At least one lowercase
        - At least one digit
        - No space
        """
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=detail)
