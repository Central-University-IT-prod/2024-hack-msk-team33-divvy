import datetime
from typing import Optional

from peewee import *
from pydantic import BaseModel


class LoginRequest(BaseModel):
    tg_id: str
    name: str
    card_number: Optional[str] = None


class CreateGroupSchema(BaseModel):
    group_name: str


class GroupSchema(BaseModel):
    group_id: int
    group_name: str
    created_by: str
    created_date: datetime.datetime
    status: str


class CreateExpenseSchema(BaseModel):
    name: str
    amount: int
    payer_user: str
    shares: list


class LoginResponse(BaseModel):
    tg_id: int
    name: str
    card_number: str
    registration_date: str
    token: str


class Debt(BaseModel):
    from_user: int
    to_user: int
    amount: int
    group: int
    confirmed_from: bool
    confirmed_to: bool


class PaymentRequestModel(BaseModel):
    from_user_id: int
    to_user_id: int
    group_id: int
    amount: float


class ExpenseResponseModel(BaseModel):
    expense_id: str
    group_id: int
    name: str
    amount: int
    to_user_id: int
    from_user_id: int
    date_created: datetime.datetime
