#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

WebPage = Union[raw.types.WebPage, raw.types.WebPageEmpty, raw.types.WebPageNotModified, raw.types.WebPagePending]


# noinspection PyRedeclaration
class WebPage:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 4 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            WebPage
            WebPageEmpty
            WebPageNotModified
            WebPagePending
    """

    QUALNAME = "haku.raw.base.WebPage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/web-page")
