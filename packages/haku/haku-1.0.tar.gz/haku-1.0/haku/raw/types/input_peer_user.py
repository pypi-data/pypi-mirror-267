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


class InputPeerUser(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputPeer`.

    Details:
        - Layer: ``177``
        - ID: ``DDE8A54C``

    Parameters:
        user_id (``int`` ``64-bit``):
            N/A

        access_hash (``int`` ``64-bit``):
            N/A

    """

    __slots__: List[str] = ["user_id", "access_hash"]

    ID = 0xdde8a54c
    QUALNAME = "types.InputPeerUser"

    def __init__(self, *, user_id: int, access_hash: int) -> None:
        self.user_id = user_id  # long
        self.access_hash = access_hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPeerUser":
        # No flags
        
        user_id = Long.read(b)
        
        access_hash = Long.read(b)
        
        return InputPeerUser(user_id=user_id, access_hash=access_hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.user_id))
        
        b.write(Long(self.access_hash))
        
        return b.getvalue()
