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


class MessageActionSecureValuesSentMe(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.MessageAction`.

    Details:
        - Layer: ``177``
        - ID: ``1B287353``

    Parameters:
        values (List of :obj:`SecureValue <haku.raw.base.SecureValue>`):
            N/A

        credentials (:obj:`SecureCredentialsEncrypted <haku.raw.base.SecureCredentialsEncrypted>`):
            N/A

    """

    __slots__: List[str] = ["values", "credentials"]

    ID = 0x1b287353
    QUALNAME = "types.MessageActionSecureValuesSentMe"

    def __init__(self, *, values: List["raw.base.SecureValue"], credentials: "raw.base.SecureCredentialsEncrypted") -> None:
        self.values = values  # Vector<SecureValue>
        self.credentials = credentials  # SecureCredentialsEncrypted

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionSecureValuesSentMe":
        # No flags
        
        values = TLObject.read(b)
        
        credentials = TLObject.read(b)
        
        return MessageActionSecureValuesSentMe(values=values, credentials=credentials)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.values))
        
        b.write(self.credentials.write())
        
        return b.getvalue()
