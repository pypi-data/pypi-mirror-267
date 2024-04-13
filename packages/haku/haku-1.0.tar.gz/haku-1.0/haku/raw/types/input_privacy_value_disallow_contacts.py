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


class InputPrivacyValueDisallowContacts(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputPrivacyRule`.

    Details:
        - Layer: ``177``
        - ID: ``BA52007``

    Parameters:
        No parameters required.

    """

    __slots__: List[str] = []

    ID = 0xba52007
    QUALNAME = "types.InputPrivacyValueDisallowContacts"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPrivacyValueDisallowContacts":
        # No flags
        
        return InputPrivacyValueDisallowContacts()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
