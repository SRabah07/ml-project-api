import json
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from db.manage_user import get_user
from auth.password import verify_password

security = HTTPBasic()


async def verify(username, password):
    """
    Verify if the given user with username and password is granted
    Parameters:
    username(str): the username
    password(str): the password

    Returns:
    bool: True if the user is granted, raise exception otherwise

    Raises: HTTPException with: status code 400 if credentials are empty, status code 401 if the user unauthorized
    """
    if not (username and password):
        raise HTTPException(status_code=403)

    # Get the user from DB
    try:
        user = await get_user(username)
    except HTTPException:
        # If user doesn't exist, it's unauthorized
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    if verify_password(password, user.password):
        return True

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
