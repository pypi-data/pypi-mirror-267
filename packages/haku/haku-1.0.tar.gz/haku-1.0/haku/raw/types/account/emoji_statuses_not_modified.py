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


class EmojiStatusesNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.account.EmojiStatuses`.

    Details:
        - Layer: ``177``
        - ID: ``D08CE645``

    Parameters:
        No parameters required.

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetDefaultEmojiStatuses
            account.GetRecentEmojiStatuses
            account.GetChannelDefaultEmojiStatuses
    """

    __slots__: List[str] = []

    ID = 0xd08ce645
    QUALNAME = "types.account.EmojiStatusesNotModified"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiStatusesNotModified":
        # No flags
        
        return EmojiStatusesNotModified()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
