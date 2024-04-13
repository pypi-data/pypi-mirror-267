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


class UpdateChannelViewForumAsMessages(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.Update`.

    Details:
        - Layer: ``177``
        - ID: ``7B68920``

    Parameters:
        channel_id (``int`` ``64-bit``):
            N/A

        enabled (``bool``):
            N/A

    """

    __slots__: List[str] = ["channel_id", "enabled"]

    ID = 0x7b68920
    QUALNAME = "types.UpdateChannelViewForumAsMessages"

    def __init__(self, *, channel_id: int, enabled: bool) -> None:
        self.channel_id = channel_id  # long
        self.enabled = enabled  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateChannelViewForumAsMessages":
        # No flags
        
        channel_id = Long.read(b)
        
        enabled = Bool.read(b)
        
        return UpdateChannelViewForumAsMessages(channel_id=channel_id, enabled=enabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.channel_id))
        
        b.write(Bool(self.enabled))
        
        return b.getvalue()
