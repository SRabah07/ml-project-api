from databases import Database
import sqlalchemy
import os

DATABASE_URL = os.environ.get('DATABASE_URL', "sqlite:///local_sqlalchemy.db")
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


def get_database() -> Database:
    return database
