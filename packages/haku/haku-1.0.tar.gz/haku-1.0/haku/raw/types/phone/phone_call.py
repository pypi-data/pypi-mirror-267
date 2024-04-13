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


class PhoneCall(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.phone.PhoneCall`.

    Details:
        - Layer: ``177``
        - ID: ``EC82E140``

    Parameters:
        phone_call (:obj:`PhoneCall <haku.raw.base.PhoneCall>`):
            N/A

        users (List of :obj:`User <haku.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 3 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            phone.RequestCall
            phone.AcceptCall
            phone.ConfirmCall
    """

    __slots__: List[str] = ["phone_call", "users"]

    ID = 0xec82e140
    QUALNAME = "types.phone.PhoneCall"

    def __init__(self, *, phone_call: "raw.base.PhoneCall", users: List["raw.base.User"]) -> None:
        self.phone_call = phone_call  # PhoneCall
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PhoneCall":
        # No flags
        
        phone_call = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return PhoneCall(phone_call=phone_call, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.phone_call.write())
        
        b.write(Vector(self.users))
        
        return b.getvalue()
