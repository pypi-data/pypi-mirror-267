#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

PublicForwards = Union[raw.types.stats.PublicForwards]


# noinspection PyRedeclaration
class PublicForwards:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            stats.PublicForwards

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            stats.GetMessagePublicForwards
            stats.GetStoryPublicForwards
    """

    QUALNAME = "haku.raw.base.stats.PublicForwards"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/public-forwards")
