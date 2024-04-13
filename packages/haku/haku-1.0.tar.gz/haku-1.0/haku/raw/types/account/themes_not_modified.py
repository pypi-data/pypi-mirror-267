#HALO INI ADALAH CLONE DARI PYROFORK.

from io import BytesIO

from haku.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from haku.raw.core import TLObject
from haku import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class ThemesNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.account.Themes`.

    Details:
        - Layer: ``177``
        - ID: ``F41EB622``

    Parameters:
        No parameters required.

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetThemes
            account.GetChatThemes
    """

    __slots__: List[str] = []

    ID = 0xf41eb622
    QUALNAME = "types.account.ThemesNotModified"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ThemesNotModified":
        # No flags
        
        return ThemesNotModified()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
