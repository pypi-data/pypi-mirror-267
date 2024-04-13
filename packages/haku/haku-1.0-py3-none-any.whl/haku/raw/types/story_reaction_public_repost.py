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


class StoryReactionPublicRepost(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.StoryReaction`.

    Details:
        - Layer: ``177``
        - ID: ``CFCD0F13``

    Parameters:
        peer_id (:obj:`Peer <haku.raw.base.Peer>`):
            N/A

        story (:obj:`StoryItem <haku.raw.base.StoryItem>`):
            N/A

    """

    __slots__: List[str] = ["peer_id", "story"]

    ID = 0xcfcd0f13
    QUALNAME = "types.StoryReactionPublicRepost"

    def __init__(self, *, peer_id: "raw.base.Peer", story: "raw.base.StoryItem") -> None:
        self.peer_id = peer_id  # Peer
        self.story = story  # StoryItem

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryReactionPublicRepost":
        # No flags
        
        peer_id = TLObject.read(b)
        
        story = TLObject.read(b)
        
        return StoryReactionPublicRepost(peer_id=peer_id, story=story)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer_id.write())
        
        b.write(self.story.write())
        
        return b.getvalue()
