from peewee import *

from database.connection import db
from database.models.expense_share import ExpenseShare
from database.models.group import Group
from database.models.group_member import GroupMember
from database.models.user import User


def create_tables():
    with db:
        db.create_tables([User, Group, GroupMember, ExpenseShare])


if __name__ == "__main__":
    create_tables()
