#HALO INI ADALAH CLONE DARI PYROFORK.

from enum import auto

from .auto_name import AutoName


class ChatMemberStatus(AutoName):
    """Chat member status enumeration used in :obj:`~haku.types.ChatMember`."""

    OWNER = auto()
    "Chat owner"

    ADMINISTRATOR = auto()
    "Chat administrator"

    MEMBER = auto()
    "Chat member"

    RESTRICTED = auto()
    "Restricted chat member"

    LEFT = auto()
    "Left chat member"

    BANNED = auto()
    "Banned chat member"
