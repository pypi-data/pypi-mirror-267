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


class ChatInviteImporters(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.messages.ChatInviteImporters`.

    Details:
        - Layer: ``177``
        - ID: ``81B6B00A``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        importers (List of :obj:`ChatInviteImporter <haku.raw.base.ChatInviteImporter>`):
            N/A

        users (List of :obj:`User <haku.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetChatInviteImporters
    """

    __slots__: List[str] = ["count", "importers", "users"]

    ID = 0x81b6b00a
    QUALNAME = "types.messages.ChatInviteImporters"

    def __init__(self, *, count: int, importers: List["raw.base.ChatInviteImporter"], users: List["raw.base.User"]) -> None:
        self.count = count  # int
        self.importers = importers  # Vector<ChatInviteImporter>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatInviteImporters":
        # No flags
        
        count = Int.read(b)
        
        importers = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ChatInviteImporters(count=count, importers=importers, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.importers))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
