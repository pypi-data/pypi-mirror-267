#HALO INI ADALAH CLONE DARI PYROFORK.

import haku
from haku import raw
from haku import types


class GetStickerSet:
    async def get_sticker_set(
        self: "haku.Client",
        set_short_name: str
    ) -> "types.StickerSet":
        """Get info about a stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            set_short_name (``str``):
               Stickerset shortname.

        Returns:
            :obj:`~haku.types.StickerSet`: On success, the StickerSet information is returned.

        Example:
            .. code-block:: python

                await app.get_sticker_set("mypack1")
        """
        r = await self.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=set_short_name),
                hash=0
            )
        )

        return types.StickerSet._parse(r.set)
