#HALO INI ADALAH CLONE DARI PYROFORK.

import haku

from ..object import Object

"""- :obj:`~haku.types.InputLocationMessageContent`
    - :obj:`~haku.types.InputVenueMessageContent`
    - :obj:`~haku.types.InputContactMessageContent`"""


class InputMessageContent(Object):
    """Content of a message to be sent as a result of an inline query.

    Haku currently supports the following types:

    - :obj:`~haku.types.InputTextMessageContent`
    """

    def __init__(self):
        super().__init__()

    async def write(self, client: "haku.Client", reply_markup):
        raise NotImplementedError
