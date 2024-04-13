#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

BoostsList = Union[raw.types.premium.BoostsList]


# noinspection PyRedeclaration
class BoostsList:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            premium.BoostsList

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            premium.GetBoostsList
            premium.GetUserBoosts
    """

    QUALNAME = "haku.raw.base.premium.BoostsList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/boosts-list")
