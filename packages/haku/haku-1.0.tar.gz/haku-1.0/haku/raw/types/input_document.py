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


class InputDocument(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputDocument`.

    Details:
        - Layer: ``177``
        - ID: ``1ABFB575``

    Parameters:
        id (``int`` ``64-bit``):
            N/A

        access_hash (``int`` ``64-bit``):
            N/A

        file_reference (``bytes``):
            N/A

    """

    __slots__: List[str] = ["id", "access_hash", "file_reference"]

    ID = 0x1abfb575
    QUALNAME = "types.InputDocument"

    def __init__(self, *, id: int, access_hash: int, file_reference: bytes) -> None:
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.file_reference = file_reference  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputDocument":
        # No flags
        
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        file_reference = Bytes.read(b)
        
        return InputDocument(id=id, access_hash=access_hash, file_reference=file_reference)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(Bytes(self.file_reference))
        
        return b.getvalue()
