import json
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

security = HTTPBasic()


#@app.middleware("http")
async def login_filter_handler(request: Request, call_next, credentials: HTTPBasicCredentials = Depends(security)):
    print(credentials)
    verify(credentials.username, credentials.password)
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def verify(username, password):
    """
    Verify if the given user with username and password is granted
    Parameters:
    username(str): the username
    password(str): the password

    Returns:
    bool: True if the user is granted, raise exception otherwise

    Raises: HTTPException with: status code 400 if credentials are empty, status code 401 if the user is not granted
    """
    if not (username and password):
        raise HTTPException(status_code=403)

    with open('../resources/credentials.json') as f:
        data = f.read()

    credentials = json.loads(data)

    if username in credentials:
        if password == credentials[username]:
            return True

    raise HTTPException(status_code=401)
