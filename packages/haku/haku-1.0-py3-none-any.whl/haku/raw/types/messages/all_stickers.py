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


class AllStickers(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.messages.AllStickers`.

    Details:
        - Layer: ``177``
        - ID: ``CDBBCEBB``

    Parameters:
        hash (``int`` ``64-bit``):
            N/A

        sets (List of :obj:`StickerSet <haku.raw.base.StickerSet>`):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetAllStickers
            messages.GetMaskStickers
            messages.GetEmojiStickers
    """

    __slots__: List[str] = ["hash", "sets"]

    ID = 0xcdbbcebb
    QUALNAME = "types.messages.AllStickers"

    def __init__(self, *, hash: int, sets: List["raw.base.StickerSet"]) -> None:
        self.hash = hash  # long
        self.sets = sets  # Vector<StickerSet>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AllStickers":
        # No flags
        
        hash = Long.read(b)
        
        sets = TLObject.read(b)
        
        return AllStickers(hash=hash, sets=sets)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.sets))
        
        return b.getvalue()
