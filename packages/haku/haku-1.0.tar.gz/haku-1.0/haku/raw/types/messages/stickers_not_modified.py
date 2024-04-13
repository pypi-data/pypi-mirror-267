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


class StickersNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.messages.Stickers`.

    Details:
        - Layer: ``177``
        - ID: ``F1749A22``

    Parameters:
        No parameters required.

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetStickers
    """

    __slots__: List[str] = []

    ID = 0xf1749a22
    QUALNAME = "types.messages.StickersNotModified"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StickersNotModified":
        # No flags
        
        return StickersNotModified()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
