#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

TopPeerCategory = Union[raw.types.TopPeerCategoryBotsInline, raw.types.TopPeerCategoryBotsPM, raw.types.TopPeerCategoryChannels, raw.types.TopPeerCategoryCorrespondents, raw.types.TopPeerCategoryForwardChats, raw.types.TopPeerCategoryForwardUsers, raw.types.TopPeerCategoryGroups, raw.types.TopPeerCategoryPhoneCalls]


# noinspection PyRedeclaration
class TopPeerCategory:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 8 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            TopPeerCategoryBotsInline
            TopPeerCategoryBotsPM
            TopPeerCategoryChannels
            TopPeerCategoryCorrespondents
            TopPeerCategoryForwardChats
            TopPeerCategoryForwardUsers
            TopPeerCategoryGroups
            TopPeerCategoryPhoneCalls
    """

    QUALNAME = "haku.raw.base.TopPeerCategory"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/top-peer-category")
