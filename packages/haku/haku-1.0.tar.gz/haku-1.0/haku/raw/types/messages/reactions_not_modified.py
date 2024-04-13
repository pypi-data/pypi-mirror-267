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


class ReactionsNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.messages.Reactions`.

    Details:
        - Layer: ``177``
        - ID: ``B06FDBDF``

    Parameters:
        No parameters required.

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetTopReactions
            messages.GetRecentReactions
            messages.GetDefaultTagReactions
    """

    __slots__: List[str] = []

    ID = 0xb06fdbdf
    QUALNAME = "types.messages.ReactionsNotModified"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReactionsNotModified":
        # No flags
        
        return ReactionsNotModified()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
