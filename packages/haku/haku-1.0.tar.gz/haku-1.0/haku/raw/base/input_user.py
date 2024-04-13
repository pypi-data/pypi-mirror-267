#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

InputUser = Union[raw.types.InputUser, raw.types.InputUserEmpty, raw.types.InputUserFromMessage, raw.types.InputUserSelf]


# noinspection PyRedeclaration
class InputUser:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 4 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            InputUser
            InputUserEmpty
            InputUserFromMessage
            InputUserSelf
    """

    QUALNAME = "haku.raw.base.InputUser"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/input-user")
