#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

UserStatus = Union[raw.types.UserStatusEmpty, raw.types.UserStatusLastMonth, raw.types.UserStatusLastWeek, raw.types.UserStatusOffline, raw.types.UserStatusOnline, raw.types.UserStatusRecently]


# noinspection PyRedeclaration
class UserStatus:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            UserStatusEmpty
            UserStatusLastMonth
            UserStatusLastWeek
            UserStatusOffline
            UserStatusOnline
            UserStatusRecently
    """

    QUALNAME = "haku.raw.base.UserStatus"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/user-status")
