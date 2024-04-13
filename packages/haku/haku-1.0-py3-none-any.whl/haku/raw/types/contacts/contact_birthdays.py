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


class ContactBirthdays(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.contacts.ContactBirthdays`.

    Details:
        - Layer: ``177``
        - ID: ``114FF30D``

    Parameters:
        contacts (List of :obj:`ContactBirthday <haku.raw.base.ContactBirthday>`):
            N/A

        users (List of :obj:`User <haku.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            contacts.GetBirthdays
    """

    __slots__: List[str] = ["contacts", "users"]

    ID = 0x114ff30d
    QUALNAME = "types.contacts.ContactBirthdays"

    def __init__(self, *, contacts: List["raw.base.ContactBirthday"], users: List["raw.base.User"]) -> None:
        self.contacts = contacts  # Vector<ContactBirthday>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ContactBirthdays":
        # No flags
        
        contacts = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return ContactBirthdays(contacts=contacts, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.contacts))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
