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


class TopPeerCategoryChannels(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.TopPeerCategory`.

    Details:
        - Layer: ``177``
        - ID: ``161D9628``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0x161d9628
    QUALNAME = "types.TopPeerCategoryChannels"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TopPeerCategoryChannels":
        # No flags
        
        return TopPeerCategoryChannels()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
