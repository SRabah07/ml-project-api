import logging
from fastapi import APIRouter, HTTPException
from password_validator import PasswordValidator
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from models import UserCreate
from db.manage_user import create_user, get_user

logger = logging.getLogger(__name__)

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


@router.post('/', status_code=HTTP_201_CREATED)
async def register(user: UserCreate):
    logger.debug(f'Register user')
    await validate(user)
    user_id = await create_user(user)
    logger.debug(f'User with id={user_id} registered')
    return user_id


async def validate(user: UserCreate):
    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User is required!")

    # Check username availability
    user_db = None
    try:
        user_db = await get_user(user.username)
    except HTTPException as e:
        if e.status_code != HTTP_404_NOT_FOUND:
            raise e

    logger.info(f'User = {user_db}')
    if user_db is not None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Username not available!")

    # Login / Username
    if len(user.username) < MIN_CHARACTERS_USERNAME:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail=f"Username/Login must be at least {MIN_CHARACTERS_USERNAME} characters")

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
