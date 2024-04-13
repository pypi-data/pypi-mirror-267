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


class SendMessageUploadDocumentAction(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.SendMessageAction`.

    Details:
        - Layer: ``177``
        - ID: ``AA0CD9E4``

    Parameters:
        progress (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["progress"]

    ID = 0xaa0cd9e4
    QUALNAME = "types.SendMessageUploadDocumentAction"

    def __init__(self, *, progress: int) -> None:
        self.progress = progress  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMessageUploadDocumentAction":
        # No flags
        
        progress = Int.read(b)
        
        return SendMessageUploadDocumentAction(progress=progress)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.progress))
        
        return b.getvalue()
