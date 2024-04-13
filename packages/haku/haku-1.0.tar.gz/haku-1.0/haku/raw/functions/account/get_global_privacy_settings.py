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


class GetGlobalPrivacySettings(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``EB2B4CF6``

    Parameters:
        No parameters required.

    Returns:
        :obj:`GlobalPrivacySettings <haku.raw.base.GlobalPrivacySettings>`
    """

    __slots__: List[str] = []

    ID = 0xeb2b4cf6
    QUALNAME = "functions.account.GetGlobalPrivacySettings"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetGlobalPrivacySettings":
        # No flags
        
        return GetGlobalPrivacySettings()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
