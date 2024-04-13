#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

SetClientDHParamsAnswer = Union[raw.types.DhGenFail, raw.types.DhGenOk, raw.types.DhGenRetry]


# noinspection PyRedeclaration
class SetClientDHParamsAnswer:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            DhGenFail
            DhGenOk
            DhGenRetry

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            SetClientDHParams
    """

    QUALNAME = "haku.raw.base.SetClientDHParamsAnswer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/set-client-dh-params-answer")
