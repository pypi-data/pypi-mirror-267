#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

ChatFull = Union[raw.types.messages.ChatFull]


# noinspection PyRedeclaration
class ChatFull:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            messages.ChatFull

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetFullChat
            channels.GetFullChannel
    """

    QUALNAME = "haku.raw.base.messages.ChatFull"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/chat-full")
