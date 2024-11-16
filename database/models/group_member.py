from peewee import *

from database.models.basemodel import BaseModel
from database.models.group import Group
from database.models.user import User


class GroupMember(BaseModel):
    group = ForeignKeyField(Group, backref="members")
    user = ForeignKeyField(User, backref="group_memberships")
    role = CharField(default="member")
    joined_date = DateTimeField()

    class Meta:
        table_name = "group_members"
        primary_key = CompositeKey("group", "user")
