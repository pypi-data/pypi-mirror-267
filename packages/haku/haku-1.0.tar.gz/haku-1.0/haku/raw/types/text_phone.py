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


class TextPhone(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.RichText`.

    Details:
        - Layer: ``177``
        - ID: ``1CCB966A``

    Parameters:
        text (:obj:`RichText <haku.raw.base.RichText>`):
            N/A

        phone (``str``):
            N/A

    """

    __slots__: List[str] = ["text", "phone"]

    ID = 0x1ccb966a
    QUALNAME = "types.TextPhone"

    def __init__(self, *, text: "raw.base.RichText", phone: str) -> None:
        self.text = text  # RichText
        self.phone = phone  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TextPhone":
        # No flags
        
        text = TLObject.read(b)
        
        phone = String.read(b)
        
        return TextPhone(text=text, phone=phone)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        b.write(String(self.phone))
        
        return b.getvalue()
