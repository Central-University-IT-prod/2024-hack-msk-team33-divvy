from fastapi import APIRouter, HTTPException, Path

from database.functions.user import get_user_by_tg_id

user_router = APIRouter()


@user_router.get("/user/{tg_id}")
async def get_groups(
    tg_id: str = Path(..., example="123456789"),
):
    try:
        user = get_user_by_tg_id(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "tg_id": user.tg_id,
        "name": user.name,
        "card_number": user.card_number,
        "registration_date": user.registration_date.isoformat(),
    }
