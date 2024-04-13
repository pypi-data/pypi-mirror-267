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


class InputPrivacyValueAllowChatParticipants(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputPrivacyRule`.

    Details:
        - Layer: ``177``
        - ID: ``840649CF``

    Parameters:
        chats (List of ``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["chats"]

    ID = 0x840649cf
    QUALNAME = "types.InputPrivacyValueAllowChatParticipants"

    def __init__(self, *, chats: List[int]) -> None:
        self.chats = chats  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPrivacyValueAllowChatParticipants":
        # No flags
        
        chats = TLObject.read(b, Long)
        
        return InputPrivacyValueAllowChatParticipants(chats=chats)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.chats, Long))
        
        return b.getvalue()
