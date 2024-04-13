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


class SetBoostsToUnblockRestrictions(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``AD399CEE``

    Parameters:
        channel (:obj:`InputChannel <haku.raw.base.InputChannel>`):
            N/A

        boosts (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`Updates <haku.raw.base.Updates>`
    """

    __slots__: List[str] = ["channel", "boosts"]

    ID = 0xad399cee
    QUALNAME = "functions.channels.SetBoostsToUnblockRestrictions"

    def __init__(self, *, channel: "raw.base.InputChannel", boosts: int) -> None:
        self.channel = channel  # InputChannel
        self.boosts = boosts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetBoostsToUnblockRestrictions":
        # No flags
        
        channel = TLObject.read(b)
        
        boosts = Int.read(b)
        
        return SetBoostsToUnblockRestrictions(channel=channel, boosts=boosts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Int(self.boosts))
        
        return b.getvalue()
