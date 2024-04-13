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


class ExportedInvites(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.chatlists.ExportedInvites`.

    Details:
        - Layer: ``177``
        - ID: ``10AB6DC7``

    Parameters:
        invites (List of :obj:`ExportedChatlistInvite <haku.raw.base.ExportedChatlistInvite>`):
            N/A

        chats (List of :obj:`Chat <haku.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <haku.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            chatlists.GetExportedInvites
    """

    __slots__: List[str] = ["invites", "chats", "users"]

    ID = 0x10ab6dc7
    QUALNAME = "types.chatlists.ExportedInvites"

    def __init__(self, *, invites: List["raw.base.ExportedChatlistInvite"], chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.invites = invites  # Vector<ExportedChatlistInvite>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedInvites":
        # No flags
        
        invites = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ExportedInvites(invites=invites, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.invites))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
