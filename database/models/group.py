from peewee import *

from database.models.basemodel import BaseModel
from database.models.user import User


class Group(BaseModel):
    group_id = AutoField(unique=True)
    group_name = CharField()
    created_by = ForeignKeyField(User, backref="created_groups")
    created_date = DateTimeField()
    closed_date = IntegerField(null=True)
    status = CharField(default="active")

    class Meta:
        table_name = "groups"
