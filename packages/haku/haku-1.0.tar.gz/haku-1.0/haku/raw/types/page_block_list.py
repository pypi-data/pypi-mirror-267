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


class PageBlockList(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.PageBlock`.

    Details:
        - Layer: ``177``
        - ID: ``E4E88011``

    Parameters:
        items (List of :obj:`PageListItem <haku.raw.base.PageListItem>`):
            N/A

    """

    __slots__: List[str] = ["items"]

    ID = 0xe4e88011
    QUALNAME = "types.PageBlockList"

    def __init__(self, *, items: List["raw.base.PageListItem"]) -> None:
        self.items = items  # Vector<PageListItem>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockList":
        # No flags
        
        items = TLObject.read(b)
        
        return PageBlockList(items=items)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.items))
        
        return b.getvalue()
