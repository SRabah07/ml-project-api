FROM python:3.8.11-alpine3.14

COPY . /test
WORKDIR test

RUN apk update --no-cache && \
    pip install  --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
