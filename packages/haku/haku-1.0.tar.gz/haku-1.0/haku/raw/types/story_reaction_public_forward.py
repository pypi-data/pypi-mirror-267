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


class StoryReactionPublicForward(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.StoryReaction`.

    Details:
        - Layer: ``177``
        - ID: ``BBAB2643``

    Parameters:
        message (:obj:`Message <haku.raw.base.Message>`):
            N/A

    """

    __slots__: List[str] = ["message"]

    ID = 0xbbab2643
    QUALNAME = "types.StoryReactionPublicForward"

    def __init__(self, *, message: "raw.base.Message") -> None:
        self.message = message  # Message

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryReactionPublicForward":
        # No flags
        
        message = TLObject.read(b)
        
        return StoryReactionPublicForward(message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.message.write())
        
        return b.getvalue()
