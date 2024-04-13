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


class PageTableRow(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.PageTableRow`.

    Details:
        - Layer: ``177``
        - ID: ``E0C0C5E5``

    Parameters:
        cells (List of :obj:`PageTableCell <haku.raw.base.PageTableCell>`):
            N/A

    """

    __slots__: List[str] = ["cells"]

    ID = 0xe0c0c5e5
    QUALNAME = "types.PageTableRow"

    def __init__(self, *, cells: List["raw.base.PageTableCell"]) -> None:
        self.cells = cells  # Vector<PageTableCell>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageTableRow":
        # No flags
        
        cells = TLObject.read(b)
        
        return PageTableRow(cells=cells)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.cells))
        
        return b.getvalue()
