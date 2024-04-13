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


class InputMediaGame(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputMedia`.

    Details:
        - Layer: ``177``
        - ID: ``D33F43F3``

    Parameters:
        id (:obj:`InputGame <haku.raw.base.InputGame>`):
            N/A

    """

    __slots__: List[str] = ["id"]

    ID = 0xd33f43f3
    QUALNAME = "types.InputMediaGame"

    def __init__(self, *, id: "raw.base.InputGame") -> None:
        self.id = id  # InputGame

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputMediaGame":
        # No flags
        
        id = TLObject.read(b)
        
        return InputMediaGame(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        return b.getvalue()
