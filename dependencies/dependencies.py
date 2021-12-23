from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth.auth import verify

import logging
import api_logging

security = HTTPBasic()


async def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    logging.debug(f'Read current user: {credentials}')
    await verify(credentials.username, credentials.password)
    return credentials.username
