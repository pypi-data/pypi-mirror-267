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


class SecurePlainPhone(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.SecurePlainData`.

    Details:
        - Layer: ``177``
        - ID: ``7D6099DD``

    Parameters:
        phone (``str``):
            N/A

    """

    __slots__: List[str] = ["phone"]

    ID = 0x7d6099dd
    QUALNAME = "types.SecurePlainPhone"

    def __init__(self, *, phone: str) -> None:
        self.phone = phone  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SecurePlainPhone":
        # No flags
        
        phone = String.read(b)
        
        return SecurePlainPhone(phone=phone)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.phone))
        
        return b.getvalue()
