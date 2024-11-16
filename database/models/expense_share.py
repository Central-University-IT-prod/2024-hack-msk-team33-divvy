from peewee import *

from database.models.basemodel import BaseModel
from database.models.group import Group
from database.models.user import User


class ExpenseShare(BaseModel):
    from_user = ForeignKeyField(User, backref="expense_shares_from")
    to_user = ForeignKeyField(User, backref="expense_shares_to")
    amount = IntegerField()
    group = ForeignKeyField(Group, backref="expense_shares")
    confirmed_from = BooleanField()
    confirmed_to = BooleanField()

    class Meta:
        table_name = "expense_shares"
