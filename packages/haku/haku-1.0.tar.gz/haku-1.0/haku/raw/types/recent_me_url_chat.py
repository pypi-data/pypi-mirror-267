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


class RecentMeUrlChat(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.RecentMeUrl`.

    Details:
        - Layer: ``177``
        - ID: ``B2DA71D2``

    Parameters:
        url (``str``):
            N/A

        chat_id (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["url", "chat_id"]

    ID = 0xb2da71d2
    QUALNAME = "types.RecentMeUrlChat"

    def __init__(self, *, url: str, chat_id: int) -> None:
        self.url = url  # string
        self.chat_id = chat_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RecentMeUrlChat":
        # No flags
        
        url = String.read(b)
        
        chat_id = Long.read(b)
        
        return RecentMeUrlChat(url=url, chat_id=chat_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Long(self.chat_id))
        
        return b.getvalue()
