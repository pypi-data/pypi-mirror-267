#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

ChatPhoto = Union[raw.types.ChatPhoto, raw.types.ChatPhotoEmpty]


# noinspection PyRedeclaration
class ChatPhoto:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            ChatPhoto
            ChatPhotoEmpty
    """

    QUALNAME = "haku.raw.base.ChatPhoto"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/chat-photo")
