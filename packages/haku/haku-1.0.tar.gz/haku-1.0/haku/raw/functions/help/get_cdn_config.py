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


class GetCdnConfig(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``52029342``

    Parameters:
        No parameters required.

    Returns:
        :obj:`CdnConfig <haku.raw.base.CdnConfig>`
    """

    __slots__: List[str] = []

    ID = 0x52029342
    QUALNAME = "functions.help.GetCdnConfig"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetCdnConfig":
        # No flags
        
        return GetCdnConfig()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
