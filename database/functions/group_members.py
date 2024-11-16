from datetime import datetime

from peewee import *

from database.functions.group import get_group_info_from_db
from database.functions.user import get_user_by_tg_id
from database.models.group_member import GroupMember


def add_user_db(tg_id: str, group_id: int):
    try:
        group = get_group_info_from_db(group_id=group_id)
        user = get_user_by_tg_id(tg_id)
    except:
        return -1
    new_gp = GroupMember.create(group=group, user=user, joined_date=datetime.now())
    return 1
