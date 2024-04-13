#HALO INI ADALAH CLONE DARI PYROFORK.

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from typing import Union
from haku import raw
from haku.raw.core import TLObject

MediaArea = Union[raw.types.InputMediaAreaChannelPost, raw.types.InputMediaAreaVenue, raw.types.MediaAreaChannelPost, raw.types.MediaAreaGeoPoint, raw.types.MediaAreaSuggestedReaction, raw.types.MediaAreaVenue]


# noinspection PyRedeclaration
class MediaArea:  # type: ignore
    """Telegram API base type.

    Constructors:
        This base type has 6 constructors available.

        .. currentmodule:: haku.raw.types

        .. autosummary::
            :nosignatures:

            InputMediaAreaChannelPost
            InputMediaAreaVenue
            MediaAreaChannelPost
            MediaAreaGeoPoint
            MediaAreaSuggestedReaction
            MediaAreaVenue
    """

    QUALNAME = "haku.raw.base.MediaArea"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes: "
                        "you tried to use a base type instance as argument, "
                        "but you need to instantiate one of its constructors instead. "
                        "More info: https://pyrofork.mayuri.my.id/telegram/base/media-area")
