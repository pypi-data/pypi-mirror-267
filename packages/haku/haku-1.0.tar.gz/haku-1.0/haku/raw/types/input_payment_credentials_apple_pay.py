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


class InputPaymentCredentialsApplePay(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.InputPaymentCredentials`.

    Details:
        - Layer: ``177``
        - ID: ``AA1C39F``

    Parameters:
        payment_data (:obj:`DataJSON <haku.raw.base.DataJSON>`):
            N/A

    """

    __slots__: List[str] = ["payment_data"]

    ID = 0xaa1c39f
    QUALNAME = "types.InputPaymentCredentialsApplePay"

    def __init__(self, *, payment_data: "raw.base.DataJSON") -> None:
        self.payment_data = payment_data  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPaymentCredentialsApplePay":
        # No flags
        
        payment_data = TLObject.read(b)
        
        return InputPaymentCredentialsApplePay(payment_data=payment_data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.payment_data.write())
        
        return b.getvalue()
