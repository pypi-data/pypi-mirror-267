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


class RecentMeUrls(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.help.RecentMeUrls`.

    Details:
        - Layer: ``177``
        - ID: ``E0310D7``

    Parameters:
        urls (List of :obj:`RecentMeUrl <haku.raw.base.RecentMeUrl>`):
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

            help.GetRecentMeUrls
    """

    __slots__: List[str] = ["urls", "chats", "users"]

    ID = 0xe0310d7
    QUALNAME = "types.help.RecentMeUrls"

    def __init__(self, *, urls: List["raw.base.RecentMeUrl"], chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.urls = urls  # Vector<RecentMeUrl>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RecentMeUrls":
        # No flags
        
        urls = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return RecentMeUrls(urls=urls, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.urls))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
