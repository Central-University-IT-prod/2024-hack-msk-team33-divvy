from peewee import *

from database.connection import db


class BaseModel(Model):
    class Meta:
        database = db
