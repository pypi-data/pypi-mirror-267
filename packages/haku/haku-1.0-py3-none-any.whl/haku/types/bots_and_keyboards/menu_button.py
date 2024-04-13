#HALO INI ADALAH CLONE DARI PYROFORK.

import haku
from haku import raw
from ..object import Object


class MenuButton(Object):
    """Describes the bot's menu button in a private chat.

    It should be one of:

    - :obj:`~haku.types.MenuButtonCommands`
    - :obj:`~haku.types.MenuButtonWebApp`
    - :obj:`~haku.types.MenuButtonDefault`

    If a menu button other than :obj:`~haku.types.MenuButtonDefault` is set for a private chat, then it is applied
    in the chat. Otherwise the default menu button is applied. By default, the menu button opens the list of bot
    commands.
    """

    def __init__(self, type: str):
        super().__init__()

        self.type = type

    async def write(self, client: "haku.Client") -> "raw.base.BotMenuButton":
        raise NotImplementedError
