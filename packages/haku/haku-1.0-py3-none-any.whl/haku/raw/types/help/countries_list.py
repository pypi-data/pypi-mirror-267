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


class CountriesList(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.help.CountriesList`.

    Details:
        - Layer: ``177``
        - ID: ``87D0759E``

    Parameters:
        countries (List of :obj:`help.Country <haku.raw.base.help.Country>`):
            N/A

        hash (``int`` ``32-bit``):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            help.GetCountriesList
    """

    __slots__: List[str] = ["countries", "hash"]

    ID = 0x87d0759e
    QUALNAME = "types.help.CountriesList"

    def __init__(self, *, countries: List["raw.base.help.Country"], hash: int) -> None:
        self.countries = countries  # Vector<help.Country>
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CountriesList":
        # No flags
        
        countries = TLObject.read(b)
        
        hash = Int.read(b)
        
        return CountriesList(countries=countries, hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.countries))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
