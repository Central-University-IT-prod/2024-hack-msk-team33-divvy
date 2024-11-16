from peewee import *

from database.models.basemodel import BaseModel
from database.models.group import Group
from database.models.user import User


class Expense(BaseModel):
    expense_id = AutoField(PrimaryKeyField(column_name="expense_id"))
    group = ForeignKeyField(Group, backref="expenses")
    name = CharField()
    amount = IntegerField()
    to_user = ForeignKeyField(User, backref="expenses_owed")
    from_user = ForeignKeyField(User, backref="expenses_paid")
    date_created = DateTimeField()

    class Meta:
        table_name = "expenses"
