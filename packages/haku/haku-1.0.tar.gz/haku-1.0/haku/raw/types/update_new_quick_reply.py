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


class UpdateNewQuickReply(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.Update`.

    Details:
        - Layer: ``177``
        - ID: ``F53DA717``

    Parameters:
        quick_reply (:obj:`QuickReply <haku.raw.base.QuickReply>`):
            N/A

    """

    __slots__: List[str] = ["quick_reply"]

    ID = 0xf53da717
    QUALNAME = "types.UpdateNewQuickReply"

    def __init__(self, *, quick_reply: "raw.base.QuickReply") -> None:
        self.quick_reply = quick_reply  # QuickReply

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateNewQuickReply":
        # No flags
        
        quick_reply = TLObject.read(b)
        
        return UpdateNewQuickReply(quick_reply=quick_reply)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.quick_reply.write())
        
        return b.getvalue()
