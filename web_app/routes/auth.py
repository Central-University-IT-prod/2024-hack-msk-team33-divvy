import jwt
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from database.functions.user import create_user, get_user_by_tg_id, update_user
from web_app.config import ALGORITHM, SECRET_KEY

from .schemas import LoginRequest, LoginResponse

login_router = APIRouter()


def generate_jwt_token(tg_id: str):
    return jwt.encode({"tg_id": tg_id}, SECRET_KEY, algorithm=ALGORITHM)


@login_router.post("/login", response_class=LoginResponse)
async def login(login_request: LoginRequest) -> LoginResponse:
    tg_id = login_request.tg_id
    name = login_request.name
    card_number = login_request.card_number

    user = get_user_by_tg_id(tg_id)
    if user:
        try:
            user = update_user(user, name, card_number)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        try:
            user = create_user(tg_id, name, card_number)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    token = generate_jwt_token(tg_id)

    response_data = {
        "tg_id": user.tg_id,
        "name": user.name,
        "card_number": user.card_number,
        "registration_date": user.registration_date.isoformat(),
        "token": token,
    }
    return JSONResponse(content=response_data)
