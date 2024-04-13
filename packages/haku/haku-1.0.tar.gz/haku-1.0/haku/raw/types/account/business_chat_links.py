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


class BusinessChatLinks(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.account.BusinessChatLinks`.

    Details:
        - Layer: ``177``
        - ID: ``EC43A2D1``

    Parameters:
        links (List of :obj:`BusinessChatLink <haku.raw.base.BusinessChatLink>`):
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

            account.GetBusinessChatLinks
    """

    __slots__: List[str] = ["links", "chats", "users"]

    ID = 0xec43a2d1
    QUALNAME = "types.account.BusinessChatLinks"

    def __init__(self, *, links: List["raw.base.BusinessChatLink"], chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.links = links  # Vector<BusinessChatLink>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BusinessChatLinks":
        # No flags
        
        links = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return BusinessChatLinks(links=links, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.links))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
