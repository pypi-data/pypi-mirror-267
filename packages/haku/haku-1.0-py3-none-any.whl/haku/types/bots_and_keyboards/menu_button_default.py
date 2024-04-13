#HALO INI ADALAH CLONE DARI PYROFORK.

import haku
from haku import raw
from .menu_button import MenuButton


class MenuButtonDefault(MenuButton):
    """Describes that no specific value for the menu button was set.
    """

    def __init__(self):
        super().__init__("default")

    async def write(self, client: "haku.Client") -> "raw.types.BotMenuButtonDefault":
        return raw.types.BotMenuButtonDefault()
