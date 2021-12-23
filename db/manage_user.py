import logging
from fastapi import HTTPException, Depends
from utils.utils import str_to_bool
from db.db import get_database, metadata, users, sqlalchemy_engine
from auth.password import encrypt_password
from models import UserCreate, User
import sqlalchemy
from sqlalchemy import select, func
import json
from databases import Database
from db.db import get_database
from starlette.status import HTTP_404_NOT_FOUND

logger = logging.getLogger(__name__)


async def init_users(database: Database):
    logger.info('Create default users...')
    count_query = select([func.count()]).select_from(users)
    logging.info(f"count_query {count_query}")
    logger.info(f"database {type(database)}")

    count_tuple = await database.fetch_one(count_query)
    if count_tuple[0] == 0:
        logging.info("Users table is empty. 'credentials.json' will be loaded")
        with open('resources/credentials.json') as file:
            persons = json.load(file)

        for key in persons.keys():
            person = persons[key]
            user = UserCreate(username=key, password=person["password"], admin=str_to_bool(person["admin"]))
            await create_user(user)
    else:
        logger.info('Users table already exist. Nothing to do!')


async def get_user(username: str) -> User:
    database = get_database()
    select_query = users.select().where(users.c.username == username)
    logger.info(f'Get user query={select_query}')
    raw_user = await database.fetch_one(select_query)
    print(f'raw_user={raw_user}')

    if raw_user is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)

    return User(**raw_user)


async def create_user(user: UserCreate):
    # FIXME see why we cannot use dependencies
    database: Database = get_database()
    hashed_password = encrypt_password(user.password)
    user_db = {"username": user.username, "password": hashed_password, "admin": user.admin}
    insert_query = users.insert().values(user_db)
    user_id = await database.execute(insert_query)
    logger.debug(f'New user created -> id={user_id}')
    return user_id
