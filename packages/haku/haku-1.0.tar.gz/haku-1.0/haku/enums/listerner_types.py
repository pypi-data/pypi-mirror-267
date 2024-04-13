#HALO INI ADALAH CLONE DARI PYROFORK.

from enum import auto

from .auto_name import AutoName


class ListenerTypes(AutoName):
    """Listener type enumeration used in :obj:`~haku.types.Client`."""

    MESSAGE = auto()
    "A Message"

    CALLBACK_QUERY = auto()
    "A CallbackQuery"
