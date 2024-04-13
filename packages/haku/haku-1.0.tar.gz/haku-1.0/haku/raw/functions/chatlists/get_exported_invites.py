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


class GetExportedInvites(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``CE03DA83``

    Parameters:
        chatlist (:obj:`InputChatlist <haku.raw.base.InputChatlist>`):
            N/A

    Returns:
        :obj:`chatlists.ExportedInvites <haku.raw.base.chatlists.ExportedInvites>`
    """

    __slots__: List[str] = ["chatlist"]

    ID = 0xce03da83
    QUALNAME = "functions.chatlists.GetExportedInvites"

    def __init__(self, *, chatlist: "raw.base.InputChatlist") -> None:
        self.chatlist = chatlist  # InputChatlist

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetExportedInvites":
        # No flags
        
        chatlist = TLObject.read(b)
        
        return GetExportedInvites(chatlist=chatlist)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chatlist.write())
        
        return b.getvalue()
