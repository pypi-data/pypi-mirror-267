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


class UpdateEncryption(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.Update`.

    Details:
        - Layer: ``177``
        - ID: ``B4A2E88D``

    Parameters:
        chat (:obj:`EncryptedChat <haku.raw.base.EncryptedChat>`):
            N/A

        date (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["chat", "date"]

    ID = 0xb4a2e88d
    QUALNAME = "types.UpdateEncryption"

    def __init__(self, *, chat: "raw.base.EncryptedChat", date: int) -> None:
        self.chat = chat  # EncryptedChat
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateEncryption":
        # No flags
        
        chat = TLObject.read(b)
        
        date = Int.read(b)
        
        return UpdateEncryption(chat=chat, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chat.write())
        
        b.write(Int(self.date))
        
        return b.getvalue()
