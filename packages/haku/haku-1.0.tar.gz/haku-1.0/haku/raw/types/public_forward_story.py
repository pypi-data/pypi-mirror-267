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


class PublicForwardStory(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.PublicForward`.

    Details:
        - Layer: ``177``
        - ID: ``EDF3ADD0``

    Parameters:
        peer (:obj:`Peer <haku.raw.base.Peer>`):
            N/A

        story (:obj:`StoryItem <haku.raw.base.StoryItem>`):
            N/A

    """

    __slots__: List[str] = ["peer", "story"]

    ID = 0xedf3add0
    QUALNAME = "types.PublicForwardStory"

    def __init__(self, *, peer: "raw.base.Peer", story: "raw.base.StoryItem") -> None:
        self.peer = peer  # Peer
        self.story = story  # StoryItem

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PublicForwardStory":
        # No flags
        
        peer = TLObject.read(b)
        
        story = TLObject.read(b)
        
        return PublicForwardStory(peer=peer, story=story)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.story.write())
        
        return b.getvalue()
