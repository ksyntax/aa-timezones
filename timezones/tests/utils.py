"""
Test utilities
"""

# Standard Library
import re
from typing import List

# Django
from django.contrib.auth.models import User

# Alliance Auth
from allianceauth.tests.auth_utils import AuthUtils


def create_fake_user(
    character_id: int,
    character_name: str,
    corporation_id: int = None,
    corporation_name: str = None,
    corporation_ticker: str = None,
    alliance_id: int = None,
    alliance_name: str = None,
    permissions: List[str] = None,
) -> User:
    """
    Create a fake user incl. main character and (optional) permissions.
    """

    username = re.sub(r"[^\w\d@\.\+-]", "_", character_name)
    user = AuthUtils.create_user(username)

    if not corporation_id:
        corporation_id = 2001
        corporation_name = "Wayne Technologies Inc."
        corporation_ticker = "WTE"

    if not alliance_id:
        alliance_id = 3001
        alliance_name = "Wayne Enterprises"

    AuthUtils.add_main_character_2(
        user=user,
        name=character_name,
        character_id=character_id,
        corp_id=corporation_id,
        corp_name=corporation_name,
        corp_ticker=corporation_ticker,
        alliance_id=alliance_id,
        alliance_name=alliance_name,
    )

    if permissions:
        perm_objs = [AuthUtils.get_permission_by_name(perm) for perm in permissions]
        user = AuthUtils.add_permissions_to_user(perms=perm_objs, user=user)

    return user
