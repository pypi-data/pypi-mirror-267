#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

ChatlistInvite = Union[raw.types.chatlists.ChatlistInvite, raw.types.chatlists.ChatlistInviteAlready]


# noinspection PyRedeclaration
class ChatlistInvite:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            chatlists.ChatlistInvite
            chatlists.ChatlistInviteAlready

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            chatlists.CheckChatlistInvite
    """

    QUALNAME = "haku.raw.base.chatlists.ChatlistInvite"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/chatlist-invite")
