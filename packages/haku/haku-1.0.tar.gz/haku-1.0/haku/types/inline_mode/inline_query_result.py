#HALO INI ADALAH CLONE DARI PYROFORK.

from uuid import uuid4

import haku
from haku import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~haku.types.InlineQueryResultCachedAudio`
    - :obj:`~haku.types.InlineQueryResultCachedDocument`
    - :obj:`~haku.types.InlineQueryResultCachedAnimation`
    - :obj:`~haku.types.InlineQueryResultCachedPhoto`
    - :obj:`~haku.types.InlineQueryResultCachedSticker`
    - :obj:`~haku.types.InlineQueryResultCachedVideo`
    - :obj:`~haku.types.InlineQueryResultCachedVoice`
    - :obj:`~haku.types.InlineQueryResultArticle`
    - :obj:`~haku.types.InlineQueryResultAudio`
    - :obj:`~haku.types.InlineQueryResultContact`
    - :obj:`~haku.types.InlineQueryResultDocument`
    - :obj:`~haku.types.InlineQueryResultAnimation`
    - :obj:`~haku.types.InlineQueryResultLocation`
    - :obj:`~haku.types.InlineQueryResultPhoto`
    - :obj:`~haku.types.InlineQueryResultVenue`
    - :obj:`~haku.types.InlineQueryResultVideo`
    - :obj:`~haku.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "haku.Client"):
        pass
