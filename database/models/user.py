import datetime

from peewee import *

from database.models.basemodel import BaseModel


class User(BaseModel):
    tg_id = CharField(unique=True)
    name = CharField()
    card_number = CharField(null=True)
    registration_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "users"
