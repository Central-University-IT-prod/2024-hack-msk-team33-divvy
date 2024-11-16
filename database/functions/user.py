import datetime
from typing import Optional

from peewee import *

from database.models.user import User


def get_user_by_tg_id(tg_id: str):
    try:
        user = User.get(User.tg_id == tg_id)
        return user
    except DoesNotExist:
        return None


def get_user_by_tg_id(tg_id: str):
    try:
        user = User.get(User.tg_id == tg_id)
        return user
    except DoesNotExist:
        return None


def create_user(tg_id: str, name: str, card_number: Optional[str]):
    registration_date = datetime.datetime.now()
    user = User.create(
        tg_id=tg_id,
        name=name,
        card_number=card_number if card_number else "",
        registration_date=registration_date,
    )
    return user


def update_user(user, name: str, card_number: Optional[str]):
    user.name = name
    if card_number is not None:
        user.card_number = card_number
    user.save()
    return user
