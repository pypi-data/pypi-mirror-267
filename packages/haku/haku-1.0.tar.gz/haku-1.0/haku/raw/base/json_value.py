#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

JSONValue = Union[raw.types.JsonArray, raw.types.JsonBool, raw.types.JsonNull, raw.types.JsonNumber, raw.types.JsonObject, raw.types.JsonString]


# noinspection PyRedeclaration
class JSONValue:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            JsonArray
            JsonBool
            JsonNull
            JsonNumber
            JsonObject
            JsonString
    """

    QUALNAME = "haku.raw.base.JSONValue"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/json-value")
