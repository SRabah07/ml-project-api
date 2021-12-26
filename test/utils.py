import requests
from requests.auth import HTTPBasicAuth
from fastapi import HTTPException, status
from datetime import datetime

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(process)d][%(processName)s][%(name)s]:%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


class APIHelper:
    def __init__(self, connection, description, output_file='api_test.log'):
        self.protocol = "http"
        if "protocol" in connection:
            self.protocol = connection["protocol"]

        if not ("host" in connection and "port" in connection):
            raise HTTPException(status_code=400, detail="Missing connection parameters!")

        self.host = connection["host"]
        self.port = connection["port"]

        logging.info(f"[port={self.port}, host={self.host}]")
        if not self.host or not self.port:
            raise HTTPException(status_code=400,
                                detail=f"Missing configuration: [host:{self.host}, port={self.port}]")

        self.url = f"{self.protocol}://{self.host}:{self.port}"
        logging.info(f"API URL = {self.url}")

        self.description = description
        self.output_file = output_file

        logging.info(f"API information: {self}")

    def __str__(self):
        data = {
            "url": self.url,
            "description": self.description,
            "output_file": self.output_file
        }
        return str(data)

    def makeRequest(self, endpoint, credentials=None, method="GET", params=None, expected=None, body=None):
        if expected is None:
            expected = {"status": "200", "message": "Success"}
        if params is None:
            params = {}

        if not endpoint:
            raise HTTPException(
                status_code=400, detail="Endpoint is missing!"
            )

        auth = {}
        if credentials is not None and len(credentials) == 2:
            auth = HTTPBasicAuth(credentials[0], credentials[1])

        url = f"{self.url}/{endpoint}"

        if method == "GET":
            req = requests.get(url, params=params, auth=auth)
        elif method in ["POST", "PUT"] and body:
            req = requests.request(method=method, url=url, auth=auth, params=params, data=body)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Method not implemented or an empty body was given. Method: {method}, Body: {body}"
            )

        actual_status_code = req.status_code
        actual_status_message = req.reason
        # content is in byte `b`
        actual_content = req.content.decode("utf-8")

        output = f'''
        ============================================
        | Date: {datetime.now()}                                    
        | Scenario: {self.description} tests       
        ============================================

        - Request information:
        | url={url}
        | method={method}
        | params={params}
        | body={body}

        - Result:
        expected status = {expected['status']}
        expected message = {expected['message']}
        ---
        actual status = {actual_status_code}
        actual message = {actual_status_message}
        actual content = {actual_content}
        '''

        logging.info(output)
        logging.info(f"Write test result into file:{self.output_file}")
        with open(self.output_file, 'a') as file:
            file.write(output)

        result = {'status': actual_status_code, 'message': actual_status_message, 'content': actual_content}
        return result
