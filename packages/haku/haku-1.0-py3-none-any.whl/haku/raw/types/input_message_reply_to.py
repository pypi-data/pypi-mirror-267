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


class InputMessageReplyTo(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputMessage`.

    Details:
        - Layer: ``177``
        - ID: ``BAD88395``

    Parameters:
        id (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["id"]

    ID = 0xbad88395
    QUALNAME = "types.InputMessageReplyTo"

    def __init__(self, *, id: int) -> None:
        self.id = id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMessageReplyTo":
        # No flags
        
        id = Int.read(b)
        
        return InputMessageReplyTo(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        return b.getvalue()
