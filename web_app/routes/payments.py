from fastapi import APIRouter, HTTPException, Query

from database.functions.expense_share import close_debt_db, confirm_payment_db

from .schemas import PaymentRequestModel

payments_router = APIRouter()


@payments_router.post("/payments", summary="Закрыть долг", tags=["Платежи"])
async def close_debt(payment_request: PaymentRequestModel):
    try:
        expense_share = close_debt_db(
            from_user_id=payment_request.from_user_id,
            to_user_id=payment_request.to_user_id,
            group_id=payment_request.group_id,
            amount=payment_request.amount,
        )
        if expense_share is None:
            raise HTTPException(status_code=404, detail="Долг не найден")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"detail": "Долг успешно закрыт"}


@payments_router.get(
    "/payments/confirm", summary="Подтвердить оплату", tags=["Платежи"]
)
async def confirm_payment(
    from_user_id: int = Query(..., description="ID отправителя"),
    to_user_id: int = Query(..., description="ID получателя"),
    group_id: int = Query(..., description="ID группы"),
):
    expense_share = confirm_payment_db(
        from_user_id=from_user_id, to_user_id=to_user_id, group_id=group_id
    )

    if expense_share is None:
        raise HTTPException(status_code=404, detail="Долг не найден")
    else:
        return {"detail": "Оплата подтверждена"}
