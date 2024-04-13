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


class SendMessageTypingAction(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.SendMessageAction`.

    Details:
        - Layer: ``177``
        - ID: ``16BF744E``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0x16bf744e
    QUALNAME = "types.SendMessageTypingAction"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMessageTypingAction":
        # No flags
        
        return SendMessageTypingAction()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
