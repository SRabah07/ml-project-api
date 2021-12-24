import logging
from fastapi import HTTPException, Depends
from db.db import get_database, metadata, models
from auth.password import encrypt_password
from models import Model
import sqlalchemy
from sqlalchemy import select, func
import json
from databases import Database
from db.db import get_database
from starlette.status import HTTP_404_NOT_FOUND
from typing import List
import csv

logger = logging.getLogger(__name__)


async def init_models(database: Database):
    logger.debug('Load models...')
    count_query = select([func.count()]).select_from(models)
    logger.debug(f"count_query {count_query}")

    count_tuple = await database.fetch_one(count_query)
    if count_tuple[0] == 0:
        logger.debug("Model table is empty. 'models_data.csv' will be loaded")
        with open('resources/models_data.csv') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                insert_query = models.insert().values(row)
                logger.debug(f'Model row: {row}, its query: {insert_query}')
                model_id = await database.execute(insert_query)
                logger.debug(f"Model inserted into database id: {model_id}")
    else:
        logger.debug('Model table already exist. Nothing to do!')


async def get(identifier: int) -> Model:
    database = get_database()
    select_query = models.select().where(models.c.id == identifier)
    logger.debug(f'Get model query={select_query}')
    raw_model = await database.fetch_one(select_query)

    if raw_model is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    logger.debug(f"Model within identifier: {identifier}, has data: {raw_model}")
    return Model(**raw_model)


async def get_by_version(version: str) -> Model:
    database = get_database()
    select_query = models.select().where(models.c.version == version)
    logger.debug(f'Get model query by version={select_query}')
    raw_model = await database.fetch_one(select_query)

    if raw_model is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return Model(**raw_model)


async def get_all() -> List[Model]:
    database = get_database()
    select_query = models.select()
    logger.debug(f'Get models query={select_query}')
    rows = await database.fetch_all(select_query)
    results = [Model(**row) for row in rows]
    return results