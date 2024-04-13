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


class ChannelAdminLogEventActionParticipantUnmute(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.ChannelAdminLogEventAction`.

    Details:
        - Layer: ``177``
        - ID: ``E64429C0``

    Parameters:
        participant (:obj:`GroupCallParticipant <haku.raw.base.GroupCallParticipant>`):
            N/A

    """

    __slots__: List[str] = ["participant"]

    ID = 0xe64429c0
    QUALNAME = "types.ChannelAdminLogEventActionParticipantUnmute"

    def __init__(self, *, participant: "raw.base.GroupCallParticipant") -> None:
        self.participant = participant  # GroupCallParticipant

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionParticipantUnmute":
        # No flags
        
        participant = TLObject.read(b)
        
        return ChannelAdminLogEventActionParticipantUnmute(participant=participant)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.participant.write())
        
        return b.getvalue()
