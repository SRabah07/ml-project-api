#FROM python:3.8.11-alpine3.14
FROM python:3.10.1-alpine3.15

COPY . /app
WORKDIR app

RUN apk update --no-cache && \
    apk add musl-dev gcc libffi-dev postgresql-dev python3-dev build-base  && \
    pip install  --no-cache-dir -r requirements.txt

EXPOSE 8000

#CMD ["uvicorn main:main --reload --port 8000 --host localhost"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Issue fixed as:
# - o matching distribution found for bcrypt==3.2.0 and exception on installing `cffi`
    # => found fix at https://pkgs.alpinelinux.org/package/edge/main/x86/py3-bcrypt and https://github.com/pyca/bcrypt =>  apk add --update musl-dev gcc libffi-dev && \
# - issue to install uvloop => Github issue (https://github.com/MagicStack/uvloop/issues/168) and fix => apk add build-base && \
# Enable to install psycopg2-binary as it uses low level c libraries. The issue only realted to Alpine =>
    # fix https://github.com/psycopg/psycopg2/issues/684 python3-dev