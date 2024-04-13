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


class MessageActionInviteToGroupCall(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.MessageAction`.

    Details:
        - Layer: ``177``
        - ID: ``502F92F7``

    Parameters:
        call (:obj:`InputGroupCall <haku.raw.base.InputGroupCall>`):
            N/A

        users (List of ``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["call", "users"]

    ID = 0x502f92f7
    QUALNAME = "types.MessageActionInviteToGroupCall"

    def __init__(self, *, call: "raw.base.InputGroupCall", users: List[int]) -> None:
        self.call = call  # InputGroupCall
        self.users = users  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionInviteToGroupCall":
        # No flags
        
        call = TLObject.read(b)
        
        users = TLObject.read(b, Long)
        
        return MessageActionInviteToGroupCall(call=call, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.call.write())
        
        b.write(Vector(self.users, Long))
        
        return b.getvalue()
