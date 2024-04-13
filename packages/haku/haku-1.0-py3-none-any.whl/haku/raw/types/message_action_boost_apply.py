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


class MessageActionBoostApply(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.MessageAction`.

    Details:
        - Layer: ``177``
        - ID: ``CC02AA6D``

    Parameters:
        boosts (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["boosts"]

    ID = 0xcc02aa6d
    QUALNAME = "types.MessageActionBoostApply"

    def __init__(self, *, boosts: int) -> None:
        self.boosts = boosts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionBoostApply":
        # No flags
        
        boosts = Int.read(b)
        
        return MessageActionBoostApply(boosts=boosts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.boosts))
        
        return b.getvalue()
