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


class AssignPlayMarketTransaction(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``177``
        - ID: ``DFFD50D3``

    Parameters:
        receipt (:obj:`DataJSON <haku.raw.base.DataJSON>`):
            N/A

        purpose (:obj:`InputStorePaymentPurpose <haku.raw.base.InputStorePaymentPurpose>`):
            N/A

    Returns:
        :obj:`Updates <haku.raw.base.Updates>`
    """

    __slots__: List[str] = ["receipt", "purpose"]

    ID = 0xdffd50d3
    QUALNAME = "functions.payments.AssignPlayMarketTransaction"

    def __init__(self, *, receipt: "raw.base.DataJSON", purpose: "raw.base.InputStorePaymentPurpose") -> None:
        self.receipt = receipt  # DataJSON
        self.purpose = purpose  # InputStorePaymentPurpose

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AssignPlayMarketTransaction":
        # No flags
        
        receipt = TLObject.read(b)
        
        purpose = TLObject.read(b)
        
        return AssignPlayMarketTransaction(receipt=receipt, purpose=purpose)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.receipt.write())
        
        b.write(self.purpose.write())
        
        return b.getvalue()
