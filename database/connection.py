from peewee import *

from database.config import db_settings

db = PostgresqlDatabase(
    db_settings.POSTGRES_DB,
    user=db_settings.POSTGRES_USER,
    password=db_settings.POSTGRES_PASSWORD,
    host=db_settings.POSTGRES_HOST,
    port=db_settings.POSTGRES_PORT,
)
