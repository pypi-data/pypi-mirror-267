#HALO INI ADALAH CLONE DARI PYROFORK.

import haku
from haku import raw
from .bot_command_scope import BotCommandScope


class BotCommandScopeAllGroupChats(BotCommandScope):
    """Represents the scope of bot commands, covering all group and supergroup chats.
    """

    def __init__(self):
        super().__init__("all_group_chats")

    async def write(self, client: "haku.Client") -> "raw.base.BotCommandScope":
        return raw.types.BotCommandScopeChats()
