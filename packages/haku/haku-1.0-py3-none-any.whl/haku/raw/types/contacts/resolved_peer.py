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


class ResolvedPeer(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.contacts.ResolvedPeer`.

    Details:
        - Layer: ``177``
        - ID: ``7F077AD9``

    Parameters:
        peer (:obj:`Peer <haku.raw.base.Peer>`):
            N/A

        chats (List of :obj:`Chat <haku.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <haku.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            contacts.ResolveUsername
            contacts.ResolvePhone
    """

    __slots__: List[str] = ["peer", "chats", "users"]

    ID = 0x7f077ad9
    QUALNAME = "types.contacts.ResolvedPeer"

    def __init__(self, *, peer: "raw.base.Peer", chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.peer = peer  # Peer
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ResolvedPeer":
        # No flags
        
        peer = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ResolvedPeer(peer=peer, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
