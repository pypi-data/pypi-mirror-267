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


class PeerStories(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.stories.PeerStories`.

    Details:
        - Layer: ``177``
        - ID: ``CAE68768``

    Parameters:
        stories (:obj:`PeerStories <haku.raw.base.PeerStories>`):
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

            stories.GetPeerStories
    """

    __slots__: List[str] = ["stories", "chats", "users"]

    ID = 0xcae68768
    QUALNAME = "types.stories.PeerStories"

    def __init__(self, *, stories: "raw.base.PeerStories", chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.stories = stories  # PeerStories
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerStories":
        # No flags
        
        stories = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return PeerStories(stories=stories, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stories.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
