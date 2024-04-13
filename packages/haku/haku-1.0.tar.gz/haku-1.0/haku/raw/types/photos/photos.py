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


class Photos(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.photos.Photos`.

    Details:
        - Layer: ``177``
        - ID: ``8DCA6AA5``

    Parameters:
        photos (List of :obj:`Photo <haku.raw.base.Photo>`):
            N/A

        users (List of :obj:`User <haku.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            photos.GetUserPhotos
    """

    __slots__: List[str] = ["photos", "users"]

    ID = 0x8dca6aa5
    QUALNAME = "types.photos.Photos"

    def __init__(self, *, photos: List["raw.base.Photo"], users: List["raw.base.User"]) -> None:
        self.photos = photos  # Vector<Photo>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Photos":
        # No flags
        
        photos = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return Photos(photos=photos, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.photos))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
