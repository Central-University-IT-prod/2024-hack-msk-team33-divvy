import datetime

from fastapi import HTTPException
from peewee import *

from database.models.group import Group
from database.models.group_member import GroupMember
from database.models.user import User
from web_app.routes.schemas import GroupSchema


def create_group_in_db(group_name: str, tg_id: str):
    try:
        user = User.get(User.tg_id == tg_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    group = Group.create(
        group_name=group_name,
        created_by=user,
        created_date=datetime.datetime.now(),
        status="active",
    )

    GroupMember.create(
        group=group, user=user, role="admin", joined_date=datetime.datetime.now()
    )

    return group.group_id


def get_user_groups_from_db(tg_id: str):
    try:
        user = User.get(User.tg_id == tg_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    group_memberships = GroupMember.select().where(GroupMember.user == user)

    groups = []
    for membership in group_memberships:
        group = membership.group
        group_info = {
            "group_id": group.group_id,
            "group_name": group.group_name,
            "created_by": group.created_by.tg_id,
            "created_date": group.created_date,
            "status": group.status,
        }
        groups.append(group_info)

    return groups


def get_group_info_from_db(group_id: int):
    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    group_info = GroupSchema(
        group_id=group.group_id,
        group_name=group.group_name,
        created_by=group.created_by.tg_id,
        created_date=group.created_date,
        status=group.status,
    )

    return group_info


def close_group_in_db(group_id: int, tg_id: str):
    try:
        user = User.get(User.tg_id == tg_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    if group.created_by != user:
        raise HTTPException(status_code=403, detail="Доступ запрещен")  # Access denied

    if group.status == "closed":
        return {"message": "Группа уже закрыта"}

    group.status = "closed"
    group.closed_date = datetime.datetime.now()
    group.save()

    return {"message": "Группа успешно закрыта"}


def check_invited_db(group_id: int, tg_id: str, user_id: str = "invited"):
    try:
        user = User.get(User.tg_id == tg_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    try:
        group_member = GroupMember.get(
            GroupMember.group == group, GroupMember.user == user
        )
    except GroupMember.DoesNotExist:
        raise HTTPException(status_code=403, detail="Доступ запрещен")


def delete_user_from_db(group_id: int, tg_id: str, user_id: str):
    try:
        current_user = User.get(User.tg_id == tg_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="Current user not found")

    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    try:
        user_to_remove = User.get(User.tg_id == user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    try:
        current_user_membership = GroupMember.get(
            GroupMember.group == group, GroupMember.user == current_user
        )
    except GroupMember.DoesNotExist:
        raise HTTPException(status_code=403, detail="Вы не являетесь членом группы")

    if group.created_by != current_user and current_user_membership.role not in [
        "admin"
    ]:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    if user_to_remove == group.created_by:
        raise HTTPException(status_code=403, detail="Нельзя удалить создателя группы")

    try:
        user_to_remove_membership = GroupMember.get(
            GroupMember.group == group, GroupMember.user == user_to_remove
        )
    except GroupMember.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="Пользователь не является участником группы"
        )

    user_to_remove_membership.delete_instance()

    return {"message": "Пользователь удален из группы"}


def get_group_members_from_db(group_id: int):
    try:
        group = Group.get(Group.group_id == group_id)
    except Group.DoesNotExist:
        raise HTTPException(status_code=404, detail="Группа не найдена")

    group_members = GroupMember.select().where(GroupMember.group == group)

    members = []
    for member in group_members:
        members.append(
            {
                "tg_id": member.user.tg_id,
                "role": member.role,
                "name": member.user.name,
                "card_number": member.user.card_number,
                "joined_date": member.joined_date,
            }
        )
    return members
