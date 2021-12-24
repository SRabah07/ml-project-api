import logging
from fastapi import Depends
from db.db import get_database, metadata, sqlalchemy_engine
from db.manage_user import init_users
from databases import Database
logger = logging.getLogger(__name__)


async def init():
    logger.info('Connect Database...')
    database = get_database()
    await database.connect()
    logger.info('Database connected...')
    logger.info('Create DB metadata...')
    metadata.create_all(sqlalchemy_engine)
    logger.info('DB metadata created...')
    logger.info('Init users...')
    await init_users(database)
    logger.info('Users initialized...')
