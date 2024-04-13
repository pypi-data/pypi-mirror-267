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


class MyBoosts(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~haku.raw.base.premium.MyBoosts`.

    Details:
        - Layer: ``177``
        - ID: ``9AE228E2``

    Parameters:
        my_boosts (List of :obj:`MyBoost <haku.raw.base.MyBoost>`):
            N/A

        chats (List of :obj:`Chat <haku.raw.base.Chat>`):
            N/A

        users (List of :obj:`User <haku.raw.base.User>`):
            N/A

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: haku.raw.functions

        .. autosummary::
            :nosignatures:

            premium.GetMyBoosts
            premium.ApplyBoost
    """

    __slots__: List[str] = ["my_boosts", "chats", "users"]

    ID = 0x9ae228e2
    QUALNAME = "types.premium.MyBoosts"

    def __init__(self, *, my_boosts: List["raw.base.MyBoost"], chats: List["raw.base.Chat"], users: List["raw.base.User"]) -> None:
        self.my_boosts = my_boosts  # Vector<MyBoost>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MyBoosts":
        # No flags
        
        my_boosts = TLObject.read(b)
        
        chats = TLObject.read(b)
        
        users = TLObject.read(b)
        
        return MyBoosts(my_boosts=my_boosts, chats=chats, users=users)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.my_boosts))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
