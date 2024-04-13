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


class UpdatePhoneCall(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.Update`.

    Details:
        - Layer: ``177``
        - ID: ``AB0F6B1E``

    Parameters:
        phone_call (:obj:`PhoneCall <haku.raw.base.PhoneCall>`):
            N/A

    """

    __slots__: List[str] = ["phone_call"]

    ID = 0xab0f6b1e
    QUALNAME = "types.UpdatePhoneCall"

    def __init__(self, *, phone_call: "raw.base.PhoneCall") -> None:
        self.phone_call = phone_call  # PhoneCall

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdatePhoneCall":
        # No flags
        
        phone_call = TLObject.read(b)
        
        return UpdatePhoneCall(phone_call=phone_call)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.phone_call.write())
        
        return b.getvalue()
