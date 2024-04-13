#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

SecurePasswordKdfAlgo = Union[raw.types.SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000, raw.types.SecurePasswordKdfAlgoSHA512, raw.types.SecurePasswordKdfAlgoUnknown]


# noinspection PyRedeclaration
class SecurePasswordKdfAlgo:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 3 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000
            SecurePasswordKdfAlgoSHA512
            SecurePasswordKdfAlgoUnknown
    """

    QUALNAME = "haku.raw.base.SecurePasswordKdfAlgo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/secure-password-kdf-algo")
