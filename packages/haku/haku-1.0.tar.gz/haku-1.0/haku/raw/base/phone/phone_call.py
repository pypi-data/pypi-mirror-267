#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

PhoneCall = Union[raw.types.phone.PhoneCall]


# noinspection PyRedeclaration
class PhoneCall:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 1 constructor available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            phone.PhoneCall

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            phone.RequestCall
            phone.AcceptCall
            phone.ConfirmCall
    """

    QUALNAME = "haku.raw.base.phone.PhoneCall"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/phone-call")
