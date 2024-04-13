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


class CheckChatlistInvite(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``41C10FFF``

    Parameters:
        slug (``str``):
            N/A

    Returns:
        :obj:`chatlists.ChatlistInvite <haku.raw.base.chatlists.ChatlistInvite>`
    """

    __slots__: List[str] = ["slug"]

    ID = 0x41c10fff
    QUALNAME = "functions.chatlists.CheckChatlistInvite"

    def __init__(self, *, slug: str) -> None:
        self.slug = slug  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckChatlistInvite":
        # No flags
        
        slug = String.read(b)
        
        return CheckChatlistInvite(slug=slug)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.slug))
        
        return b.getvalue()
