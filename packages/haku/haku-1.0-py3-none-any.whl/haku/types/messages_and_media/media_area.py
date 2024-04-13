#HALO INI ADALAH CLONE DARI PYROFORK.

import haku

from haku import raw, types
from ..object import Object


class MediaArea(Object):
    """Content of a media areas in story.

    It should be one of:

    - :obj:`~haku.types.MediaAreaChannelPost`
    """

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates"
    ):
        super().__init__()

        self.coordinates = coordinates

    async def _parse(
        client: "haku.Client",
        media_area: "raw.base.MediaArea"
    ) -> "MediaArea":
        if isinstance(media_area, raw.types.MediaAreaChannelPost):
            return await types.MediaAreaChannelPost._parse(client, media_area)
