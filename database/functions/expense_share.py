from typing import List, Optional

from peewee import *

from database.models.expense_share import ExpenseShare
from database.models.group import Group


def get_expense_shares_by_group(group_id: int) -> Optional[List[ExpenseShare]]:
    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        return None

    expense_shares = ExpenseShare.select().where(ExpenseShare.group == group).execute()
    return list(expense_shares)


def close_debt_db(from_user_id: int, to_user_id: int, group_id: int, amount: float):
    try:
        expense_share = ExpenseShare.get(
            (ExpenseShare.from_user_id == from_user_id)
            & (ExpenseShare.to_user_id == to_user_id)
            & (ExpenseShare.group_id == group_id)
        )
    except ExpenseShare.DoesNotExist:
        return None

    if expense_share.amount != amount:
        raise ValueError("Некорректная сумма долга")

    # Set confirmed_from to True
    expense_share.confirmed_from = True
    expense_share.save()

    if expense_share.confirmed_from and expense_share.confirmed_to:
        expense_share.delete_instance()

    return expense_share


def confirm_payment_db(from_user_id: int, to_user_id: int, group_id: int):
    try:
        expense_share = ExpenseShare.get(
            (ExpenseShare.from_user_id == from_user_id)
            & (ExpenseShare.to_user_id == to_user_id)
            & (ExpenseShare.group_id == group_id)
        )
    except ExpenseShare.DoesNotExist:
        return None

    expense_share.confirmed_to = True
    expense_share.save()

    if expense_share.confirmed_from and expense_share.confirmed_to:
        expense_share.delete_instance()

    return expense_share
