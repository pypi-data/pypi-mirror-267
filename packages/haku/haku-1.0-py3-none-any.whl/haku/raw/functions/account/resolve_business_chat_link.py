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


class ResolveBusinessChatLink(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``5492E5EE``

    Parameters:
        slug (``str``):
            N/A

    Returns:
        :obj:`account.ResolvedBusinessChatLinks <haku.raw.base.account.ResolvedBusinessChatLinks>`
    """

    __slots__: List[str] = ["slug"]

    ID = 0x5492e5ee
    QUALNAME = "functions.account.ResolveBusinessChatLink"

    def __init__(self, *, slug: str) -> None:
        self.slug = slug  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ResolveBusinessChatLink":
        # No flags
        
        slug = String.read(b)
        
        return ResolveBusinessChatLink(slug=slug)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.slug))
        
        return b.getvalue()
