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


class SavedReactionTags(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.messages.SavedReactionTags`.

    Details:
        - Layer: ``177``
        - ID: ``3259950A``

    Parameters:
        tags (List of :obj:`SavedReactionTag <haku.raw.base.SavedReactionTag>`):
            N/A

        hash (``int`` ``64-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetSavedReactionTags
    """

    __slots__: List[str] = ["tags", "hash"]

    ID = 0x3259950a
    QUALNAME = "types.messages.SavedReactionTags"

    def __init__(self, *, tags: List["raw.base.SavedReactionTag"], hash: int) -> None:
        self.tags = tags  # Vector<SavedReactionTag>
        self.hash = hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SavedReactionTags":
        # No flags
        
        tags = TLObject.read(b)
        
        hash = Long.read(b)
        
        return SavedReactionTags(tags=tags, hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.tags))
        
        b.write(Long(self.hash))
        
        return b.getvalue()
