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


class ChannelAdminLogEventActionParticipantInvite(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.ChannelAdminLogEventAction`.

    Details:
        - Layer: ``177``
        - ID: ``E31C34D8``

    Parameters:
        participant (:obj:`ChannelParticipant <haku.raw.base.ChannelParticipant>`):
            N/A

    """

    __slots__: List[str] = ["participant"]

    ID = 0xe31c34d8
    QUALNAME = "types.ChannelAdminLogEventActionParticipantInvite"

    def __init__(self, *, participant: "raw.base.ChannelParticipant") -> None:
        self.participant = participant  # ChannelParticipant

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionParticipantInvite":
        # No flags
        
        participant = TLObject.read(b)
        
        return ChannelAdminLogEventActionParticipantInvite(participant=participant)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.participant.write())
        
        return b.getvalue()
