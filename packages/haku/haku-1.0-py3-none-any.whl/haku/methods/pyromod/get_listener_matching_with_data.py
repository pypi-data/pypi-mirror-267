#HALO INI ADALAH CLONE DARI PYROFORK.

import haku

from typing import Optional
from haku.types import Identifier, Listener

class GetListenerMatchingWithData:
    def get_listener_matching_with_data(
        self: "haku.Client",
        data: Identifier,
        listener_type: "haku.enums.ListenerTypes"
    ) -> Optional[Listener]:
        """Gets a listener that matches the given data.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            data (:obj:`~haku.types.Identifier`):
                The Identifier to match agains.

            listener_type (:obj:`~haku.enums.ListenerTypes`):
                The type of listener to get.

        Returns:
            :obj:`~haku.types.Listener`: On success, a Listener is returned.
        """
        matching = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                matching.append(listener)

        # in case of multiple matching listeners, the most specific should be returned
        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)
