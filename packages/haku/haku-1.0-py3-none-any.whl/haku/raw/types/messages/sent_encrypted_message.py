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


class SentEncryptedMessage(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.messages.SentEncryptedMessage`.

    Details:
        - Layer: ``177``
        - ID: ``560F8935``

    Parameters:
        date (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.SendEncrypted
            messages.SendEncryptedFile
            messages.SendEncryptedService
    """

    __slots__: List[str] = ["date"]

    ID = 0x560f8935
    QUALNAME = "types.messages.SentEncryptedMessage"

    def __init__(self, *, date: int) -> None:
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SentEncryptedMessage":
        # No flags
        
        date = Int.read(b)
        
        return SentEncryptedMessage(date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        return b.getvalue()
