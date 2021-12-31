from databases import Database
import sqlalchemy
import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_DB = "sqlite:///ml_sentiment.db"

DATABASE_TEMPLATE = os.environ.get('DB_TEMPLATE')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = os.environ.get('DATABASE_PORT')

logger.debug(
    f"DATABASE_TEMPLATE={DATABASE_TEMPLATE}"
    f"DATABASE_HOST={DATABASE_HOST}, DATABASE_PORT={DATABASE_PORT}, PASSWORD={os.environ.get('POSTGRES_USER', '')}, "
    f"LOGIN={os.environ.get('POSTGRES_PASSWORD', '')} ")



if not DATABASE_TEMPLATE:
    logger.warn(
        """
        No Database template provided. Available are: [postgres]
        > -- Local Sqlite DB will be used. -- <
        """
    )
elif not (DATABASE_HOST or DATABASE_PORT):
    raise Exception(f"Template provide={DATABASE_TEMPLATE}. But no Database host / port found")


def build_db_url() -> str:
    if DATABASE_TEMPLATE and DATABASE_TEMPLATE.lower() == "postgres":
        user = os.environ.get('POSTGRES_USER', '')
        password = os.environ.get('POSTGRES_PASSWORD', '')
        if not user:
            logger.warn("No user provided for the DB.")
        if not password:
            logger.warn("No password provided for the DB.")

        url = f"postgresql://{user}:{password}@{DATABASE_HOST}:{DATABASE_PORT}/"
        logger.warn(f"URL is: {url}")
        return url

    return DEFAULT_DB


DATABASE_URL = build_db_url()
logger.info(f"Database URL: {DATABASE_URL}")
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("username", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("admin", sqlalchemy.Boolean, nullable=False),
)

models = sqlalchemy.Table(
    "model",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("key", sqlalchemy.String(length=100), nullable=False),
    sqlalchemy.Column("version", sqlalchemy.String(length=3), nullable=False),
    sqlalchemy.Column("type", sqlalchemy.String(length=50), nullable=False),
    sqlalchemy.Column("model", sqlalchemy.String(length=150), nullable=False),
    sqlalchemy.Column("branch", sqlalchemy.String(length=100), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(length=250), nullable=False),
    sqlalchemy.Column("score", sqlalchemy.Numeric(), nullable=False),
)


def get_database() -> Database:
    return database
