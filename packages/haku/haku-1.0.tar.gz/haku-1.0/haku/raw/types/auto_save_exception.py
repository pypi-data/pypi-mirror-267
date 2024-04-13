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


class AutoSaveException(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.AutoSaveException`.

    Details:
        - Layer: ``177``
        - ID: ``81602D47``

    Parameters:
        peer (:obj:`Peer <haku.raw.base.Peer>`):
            N/A

        settings (:obj:`AutoSaveSettings <haku.raw.base.AutoSaveSettings>`):
            N/A

    """

    __slots__: List[str] = ["peer", "settings"]

    ID = 0x81602d47
    QUALNAME = "types.AutoSaveException"

    def __init__(self, *, peer: "raw.base.Peer", settings: "raw.base.AutoSaveSettings") -> None:
        self.peer = peer  # Peer
        self.settings = settings  # AutoSaveSettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AutoSaveException":
        # No flags
        
        peer = TLObject.read(b)
        
        settings = TLObject.read(b)
        
        return AutoSaveException(peer=peer, settings=settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.settings.write())
        
        return b.getvalue()
