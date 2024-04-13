#HALO INI ADALAH CLONE DARI PYROFORK.

import haku

from typing import List
from haku.types import Identifier, Listener

class GetManyListenersMatchingWithData:
    def get_many_listeners_matching_with_data(
        self: "haku.Client",
        data: Identifier,
        listener_type: "haku.enums.ListenerTypes",
    ) -> List[Listener]:
        """Gets multiple listener that matches the given data.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            data (:obj:`~haku.types.Identifier`):
                The Identifier to match agains.

            listener_type (:obj:`~haku.enums.ListenerTypes`):
                The type of listener to get.

        Returns:
            List of :obj:`~haku.types.Listener`: On success, a list of Listener is returned.
        """
        listeners = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                listeners.append(listener)
        return listeners
