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


class GetGiveawayInfo(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``F4239425``

    Parameters:
        peer (:obj:`InputPeer <haku.raw.base.InputPeer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

    Returns:
        :obj:`payments.GiveawayInfo <haku.raw.base.payments.GiveawayInfo>`
    """

    __slots__: List[str] = ["peer", "msg_id"]

    ID = 0xf4239425
    QUALNAME = "functions.payments.GetGiveawayInfo"

    def __init__(self, *, peer: "raw.base.InputPeer", msg_id: int) -> None:
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetGiveawayInfo":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        return GetGiveawayInfo(peer=peer, msg_id=msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        return b.getvalue()
