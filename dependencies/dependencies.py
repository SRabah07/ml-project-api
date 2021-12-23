from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth import verify
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(process)d][%(processName)s][%(name)s]:%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../api.log"),
        logging.StreamHandler()
    ]
)

security = HTTPBasic()


def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    logging.debug(f'Read current user: {credentials}')
    verify(credentials.username, credentials.password)
    return credentials.username
