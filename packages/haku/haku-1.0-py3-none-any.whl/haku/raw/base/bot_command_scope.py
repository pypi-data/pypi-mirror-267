#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

BotCommandScope = Union[raw.types.BotCommandScopeChatAdmins, raw.types.BotCommandScopeChats, raw.types.BotCommandScopeDefault, raw.types.BotCommandScopePeer, raw.types.BotCommandScopePeerAdmins, raw.types.BotCommandScopePeerUser, raw.types.BotCommandScopeUsers]


# noinspection PyRedeclaration
class BotCommandScope:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 7 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            BotCommandScopeChatAdmins
            BotCommandScopeChats
            BotCommandScopeDefault
            BotCommandScopePeer
            BotCommandScopePeerAdmins
            BotCommandScopePeerUser
            BotCommandScopeUsers
    """

    QUALNAME = "haku.raw.base.BotCommandScope"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/bot-command-scope")
