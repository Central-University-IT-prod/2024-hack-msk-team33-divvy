import base64
from typing import List

import jwt
from fastapi import APIRouter, Header, HTTPException, Path, Query

from database.functions.group import (
    check_invited_db,
    close_group_in_db,
    create_group_in_db,
    delete_user_from_db,
    get_group_info_from_db,
    get_group_members_from_db,
    get_user_groups_from_db,
)
from web_app.config import ALGORITHM, SECRET_KEY

from .schemas import CreateGroupSchema, GroupSchema

group_router = APIRouter()


@group_router.post("/groups", status_code=201)
def create_group_api(request: CreateGroupSchema, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = jwt.decode(authorization.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
    tg_id = payload.get("tg_id")
    group_name = request.group_name

    group_id = create_group_in_db(group_name, tg_id)

    return {"message": "Group created", "group_id": group_id}


@group_router.get("/groups", response_model=List[GroupSchema])
async def get_groups(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = jwt.decode(authorization.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
    tg_id = payload.get("tg_id")
    groups = get_user_groups_from_db(tg_id)

    return groups


@group_router.get("/groups/{group_id}", response_model=GroupSchema)
async def get_group_info(group_id: int = Path(..., example=1)):
    group_info = get_group_info_from_db(group_id)
    return group_info


@group_router.patch("/groups/{group_id}")
async def close_group(
    group_id: int = Path(..., example=1), authorization: str = Header(None)
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = jwt.decode(authorization.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
    tg_id = payload.get("tg_id")
    result = close_group_in_db(group_id, tg_id)
    return result


def encode_group_id(group_id: int) -> str:
    group_id_bytes = str(group_id).encode("utf-8")
    encoded_bytes = base64.urlsafe_b64encode(group_id_bytes)
    encoded_str = encoded_bytes.decode("utf-8").rstrip("=")
    return encoded_str


@group_router.post("/groups/{group_id}/invite")
async def create_invite_link(
    group_id: int = Path(..., example=1), authorization: str = Header(None)
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = jwt.decode(authorization.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
    tg_id = payload.get("tg_id")
    check_invited_db(group_id, tg_id)
    encoded_group_id = encode_group_id(group_id)
    invite_link = f"https://t.me/{{sensitive_data}}?start={encoded_group_id}"

    return {"invite_link": invite_link}


@group_router.delete("/groups/{group_id}/remove_user")
async def remove_user_from_group(
    group_id: int = Path(..., example=1),
    user_id: str = Query(..., alias="user_id", example="123456789"),
    authorization: str = Header(None),
):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = jwt.decode(authorization.split()[1], SECRET_KEY, algorithms=[ALGORITHM])
    tg_id = payload.get("tg_id")
    return delete_user_from_db(group_id, user_id, tg_id)


@group_router.get("/groups/{group_id}/members")
async def get_group_members(group_id: int = Path(..., example=1)):
    return get_user_groups_from_db(group_id)
