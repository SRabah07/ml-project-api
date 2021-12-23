import logging
import api_logging
from fastapi import Depends
from db.db import get_database, metadata, sqlalchemy_engine
from db.manage_user import init_users
from databases import Database


async def init():
    logging.info('Connect Database...')
    database = get_database()
    await database.connect()
    logging.info('Database connected...')
    logging.info('Create DB metadata...')
    metadata.create_all(sqlalchemy_engine)
    logging.info('DB metadata created...')
    logging.info('Init users...')
    await init_users(database)
    logging.info('Users inited...')
