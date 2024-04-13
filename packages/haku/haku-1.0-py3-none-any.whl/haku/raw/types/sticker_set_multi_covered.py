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


class StickerSetMultiCovered(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.StickerSetCovered`.

    Details:
        - Layer: ``177``
        - ID: ``3407E51B``

    Parameters:
        set (:obj:`StickerSet <haku.raw.base.StickerSet>`):
            N/A

        covers (List of :obj:`Document <haku.raw.base.Document>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetAttachedStickers
    """

    __slots__: List[str] = ["set", "covers"]

    ID = 0x3407e51b
    QUALNAME = "types.StickerSetMultiCovered"

    def __init__(self, *, set: "raw.base.StickerSet", covers: List["raw.base.Document"]) -> None:
        self.set = set  # StickerSet
        self.covers = covers  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StickerSetMultiCovered":
        # No flags
        
        set = TLObject.read(b)
        
        covers = TLObject.read(b)
        
        return StickerSetMultiCovered(set=set, covers=covers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.set.write())
        
        b.write(Vector(self.covers))
        
        return b.getvalue()
