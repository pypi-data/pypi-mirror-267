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


class ChannelAdminLogEventActionDeleteMessage(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.ChannelAdminLogEventAction`.

    Details:
        - Layer: ``177``
        - ID: ``42E047BB``

    Parameters:
        message (:obj:`Message <haku.raw.base.Message>`):
            N/A

    """

    __slots__: List[str] = ["message"]

    ID = 0x42e047bb
    QUALNAME = "types.ChannelAdminLogEventActionDeleteMessage"

    def __init__(self, *, message: "raw.base.Message") -> None:
        self.message = message  # Message

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionDeleteMessage":
        # No flags
        
        message = TLObject.read(b)
        
        return ChannelAdminLogEventActionDeleteMessage(message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.message.write())
        
        return b.getvalue()
