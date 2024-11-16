import heapq
from collections import defaultdict
from typing import List
from uuid import uuid4

import jwt
from fastapi import APIRouter, Header, HTTPException, Path

from database.functions.expense import (
    create_expense,
    delete_shared_expense,
    get_all_expences,
    get_old_expences_list,
    make_shared_expense,
)
from database.functions.user import get_user_by_tg_id
from web_app.config import ALGORITHM, SECRET_KEY

from .schemas import CreateExpenseSchema, ExpenseResponseModel

expence_router = APIRouter()


def simplify_debts(transactions):
    balances = defaultdict(int)

    for transaction in transactions:
        debtor, creditor, amount = transaction
        balances[debtor] -= amount
        balances[creditor] += amount

    creditors = []
    debtors = []

    for person, balance in balances.items():
        if balance > 0:
            creditors.append((-balance, person))
        elif balance < 0:
            debtors.append((balance, person))

    heapq.heapify(creditors)
    heapq.heapify(debtors)
    result_transactions = []

    while creditors and debtors:
        creditor_amount, creditor_name = heapq.heappop(creditors)
        debtor_amount, debtor_name = heapq.heappop(debtors)

        transaction_amount = min(-creditor_amount, -debtor_amount)
        result_transactions.append((debtor_name, creditor_name, transaction_amount))

        creditor_amount += transaction_amount
        debtor_amount += transaction_amount

        if creditor_amount < 0:
            heapq.heappush(creditors, (creditor_amount, creditor_name))
        if debtor_amount < 0:
            heapq.heappush(debtors, (debtor_amount, debtor_name))

    return result_transactions


@expence_router.post("/expense/{group_id}")
async def make_expense(
    request: CreateExpenseSchema,
    group_id: int = Path(..., example=1),
    authorization: str = Header(None),
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = jwt.decode(authorization.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
    tg_id = payload.get("tg_id")
    new_expenses_list = []
    expension_id = str(uuid4())
    for user_from in request.shares:
        new_expenses_list.append([user_from, tg_id, request.amount])
        create_expense(
            request.name, request.amount, user_from, tg_id, group_id, expension_id
        )

    old_expences_list = get_old_expences_list(group_id)

    delete_shared_expense(group_id)
    transactions = simplify_debts(old_expences_list + new_expenses_list)

    for debtor, creditor, amount in transactions:
        make_shared_expense(debtor, creditor, amount, group_id)

    return {"message": "Expense created"}


@expence_router.get("/expense/{group_id}", response_model=List[ExpenseResponseModel])
async def get_expense(
    group_id: int = Path(..., example=1),
):
    expenses = get_all_expences(group_id)
    serialized_expenses = []
    for expense in expenses:
        serialized_expenses.append(
            {
                "expense_id": expense.expense_id,
                "group_id": expense.group,
                "name": expense.name,
                "amount": expense.amount,
                "to_user_id": expense.to_user,
                "from_user_id": expense.from_user,
                "date_created": expense.date_created,
            }
        )
    grouped_expenses = {}

    for expense in expenses:
        if expense.expense_id not in grouped_expenses:
            grouped_expenses[expense.expense_id] = []
        grouped_expenses[expense.expense_id].append(
            {
                "group_id": expense.group,
                "name": expense.name,
                "amount": expense.amount,
                "to_user_id": expense.to_user,
                "from_user_name": get_user_by_tg_id(expense.from_user).name,
                "to_user_name": get_user_by_tg_id(expense.to_user).name,
                "from_user_id": expense.from_user,
                "date_created": expense.date_created,
            }
        )

    return grouped_expenses
