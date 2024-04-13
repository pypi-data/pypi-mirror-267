#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

WallPaper = Union[raw.types.WallPaper, raw.types.WallPaperNoFile]


# noinspection PyRedeclaration
class WallPaper:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 2 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            WallPaper
            WallPaperNoFile

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetWallPaper
            account.UploadWallPaper
            account.GetMultiWallPapers
    """

    QUALNAME = "haku.raw.base.WallPaper"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/wall-paper")
