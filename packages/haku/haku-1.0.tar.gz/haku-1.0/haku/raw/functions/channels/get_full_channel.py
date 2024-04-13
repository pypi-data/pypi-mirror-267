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


class GetFullChannel(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``8736A09``

    Parameters:
        channel (:obj:`InputChannel <haku.raw.base.InputChannel>`):
            N/A

    Returns:
        :obj:`messages.ChatFull <haku.raw.base.messages.ChatFull>`
    """

    __slots__: List[str] = ["channel"]

    ID = 0x8736a09
    QUALNAME = "functions.channels.GetFullChannel"

    def __init__(self, *, channel: "raw.base.InputChannel") -> None:
        self.channel = channel  # InputChannel

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetFullChannel":
        # No flags
        
        channel = TLObject.read(b)
        
        return GetFullChannel(channel=channel)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        return b.getvalue()
