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


class DialogFilterDefault(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.DialogFilter`.

    Details:
        - Layer: ``177``
        - ID: ``363293AE``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0x363293ae
    QUALNAME = "types.DialogFilterDefault"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DialogFilterDefault":
        # No flags
        
        return DialogFilterDefault()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
