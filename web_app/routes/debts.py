from typing import List

from fastapi import APIRouter, HTTPException

from database.functions.expense_share import get_expense_shares_by_group

from .schemas import Debt

depts_router = APIRouter()


@depts_router.get(
    "/debts/{group_id}",
    response_model=List[Debt],
    summary="Получить задолженности по группе",
    tags=["Долги"],
)
async def get_group_debts(group_id: int):
    expense_shares = get_expense_shares_by_group(group_id)
    if expense_shares is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    debts = []
    for share in expense_shares:
        debt = Debt(
            from_user=share.from_user.id,
            to_user=share.to_user.id,
            amount=share.amount,
            group=share.group.id,
            confirmed_from=share.confirmed_from,
            confirmed_to=share.confirmed_to,
        )
        debts.append(debt)

    return debts
