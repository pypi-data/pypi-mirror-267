#HALO INI ADALAH CLONE DARI PYROFORK.

from enum import auto

from .auto_name import AutoName


class StoriesPrivacyRules(AutoName):
    """Stories privacy rules type enumeration used in :meth:`~haku.Client.send_story` and :meth:`~haku.Client.edit_story`."""

    PUBLIC = auto()
    "Public stories"

    CLOSE_FRIENDS = auto()
    "Close_Friends stories"

    CONTACTS = auto()
    "Contacts only stories"

    PRIVATE = auto()
    "Private stories"

    NO_CONTACTS = auto()
    "Hide stories from contacts"
