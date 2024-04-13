#HALO INI ADALAH CLONE DARI PYROFORK.

import haku
from haku.types import Listener

class RemoveListener:
    def remove_listener(
        self: "haku.Client",
        listener: Listener
    ):
        """Removes a listener from the :meth:`~haku.Client.listeners` dictionary.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            listener (:obj:`~haku.types.Listener`):
                The listener to remove.
        """
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass
