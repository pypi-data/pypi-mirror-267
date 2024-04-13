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


class InputPrivacyValueDisallowUsers(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputPrivacyRule`.

    Details:
        - Layer: ``177``
        - ID: ``90110467``

    Parameters:
        users (List of :obj:`InputUser <haku.raw.base.InputUser>`):
            N/A

    """

    __slots__: List[str] = ["users"]

    ID = 0x90110467
    QUALNAME = "types.InputPrivacyValueDisallowUsers"

    def __init__(self, *, users: List["raw.base.InputUser"]) -> None:
        self.users = users  # Vector<InputUser>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPrivacyValueDisallowUsers":
        # No flags
        
        users = TLObject.read(b)
        
        return InputPrivacyValueDisallowUsers(users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.users))
        
        return b.getvalue()
