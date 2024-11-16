from fastapi import HTTPException
from peewee import *

from database.models.expense import Expense
from database.models.expense_share import ExpenseShare
from database.models.group import Group
from database.models.group_member import GroupMember
from database.models.user import User


def create_expense(
    name: str,
    amount: float,
    user_from: int,
    user_to: int,
    group_id: int,
    expension_id: str,
):
    if user_from == user_to:
        raise HTTPException(
            status_code=400,
            detail="Плательщик и получатель не могут быть одним и тем же пользователем.",
        )

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Сумма должна быть больше 0.")

    try:
        from_user = User.get(User.tg_id == user_from)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="Пользователь-отправитель не найден."
        )

    try:
        to_user = User.get(User.tg_id == user_to)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="Пользователь-получатель не найден."
        )

    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена.")

    try:
        GroupMember.get(GroupMember.group == group, GroupMember.user == from_user)
        GroupMember.get(GroupMember.group == group, GroupMember.user == to_user)
    except GroupMember.DoesNotExist:
        raise HTTPException(
            status_code=400,
            detail="Один или оба пользователя не являются членами группы.",
        )

    try:
        Expense.create(
            expense_id=expension_id,
            name=name,
            amount=amount,
            from_user=from_user,
            to_user=to_user,
            group=group,
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Ошибка при создании записи о расходе."
        )


def get_old_expences_list(group_id: int):
    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена.")

    expenses = []
    for expense in ExpenseShare.select().where(ExpenseShare.group == group):
        expenses.append([expense.from_user, expense.to_user, expense.amount])

    return expenses


def delete_shared_expense(group_id: int):
    try:
        ExpenseShare.delete().where(ExpenseShare.group == group_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Ошибка при удалении записи о расходе."
        )


def make_shared_expense(from_user: int, to_user: int, amount: float, group_id: int):
    try:
        ExpenseShare.create(
            from_user=from_user, to_user=to_user, amount=amount, group=group_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Ошибка при создании записи о расходе."
        )


def get_all_expences(group_id: int):
    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена.")

    return Expense.select().where(Expense.group == group)
