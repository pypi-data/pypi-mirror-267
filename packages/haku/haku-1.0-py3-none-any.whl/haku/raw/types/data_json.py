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


class DataJSON(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.DataJSON`.

    Details:
        - Layer: ``177``
        - ID: ``7D748D04``

    Parameters:
        data (``str``):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            bots.SendCustomRequest
            bots.InvokeWebViewCustomMethod
            phone.GetCallConfig
    """

    __slots__: List[str] = ["data"]

    ID = 0x7d748d04
    QUALNAME = "types.DataJSON"

    def __init__(self, *, data: str) -> None:
        self.data = data  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DataJSON":
        # No flags
        
        data = String.read(b)
        
        return DataJSON(data=data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.data))
        
        return b.getvalue()
