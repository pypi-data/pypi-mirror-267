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


class UpdateBotBusinessConnect(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.Update`.

    Details:
        - Layer: ``177``
        - ID: ``8AE5C97A``

    Parameters:
        connection (:obj:`BotBusinessConnection <haku.raw.base.BotBusinessConnection>`):
            N/A

        qts (``int`` ``32-bit``):
            N/A

    """

    __slots__: List[str] = ["connection", "qts"]

    ID = 0x8ae5c97a
    QUALNAME = "types.UpdateBotBusinessConnect"

    def __init__(self, *, connection: "raw.base.BotBusinessConnection", qts: int) -> None:
        self.connection = connection  # BotBusinessConnection
        self.qts = qts  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateBotBusinessConnect":
        # No flags
        
        connection = TLObject.read(b)
        
        qts = Int.read(b)
        
        return UpdateBotBusinessConnect(connection=connection, qts=qts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.connection.write())
        
        b.write(Int(self.qts))
        
        return b.getvalue()
