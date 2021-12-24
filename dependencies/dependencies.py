from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth.auth import verify
import logging

logger = logging.getLogger(__name__)

security = HTTPBasic()


async def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    await verify(credentials.username, credentials.password)
    return credentials.username
