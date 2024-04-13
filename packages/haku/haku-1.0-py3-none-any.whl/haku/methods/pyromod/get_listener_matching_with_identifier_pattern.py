#HALO INI ADALAH CLONE DARI PYROFORK.

import haku

from typing import Optional
from haku.types import Identifier, Listener

class GetListenerMatchingWithIdentifierPattern:
    def get_listener_matching_with_identifier_pattern(
        self: "haku.Client",
        pattern: Identifier,
        listener_type: "haku.enums.ListenerTypes"
    ) -> Optional[Listener]:
        """Gets a listener that matches the given identifier pattern.

        .. include:: /_includes/usable-by/users-bots.rst

        The difference from :meth:`~haku.Client.get_listener_matching_with_data` is that this method
        intends to get a listener by passing partial info of the listener identifier, while the other method
        intends to get a listener by passing the full info of the update data, which the listener should match with.

        Parameters:
            pattern (:obj:`~haku.types.Identifier`):
                The Identifier to match agains.

            listener_type (:obj:`~haku.enums.ListenerTypes`):
                The type of listener to get.

        Returns:
            :obj:`~haku.types.Listener`: On success, a Listener is returned.
        """
        matching = []
        for listener in self.listeners[listener_type]:
            if pattern.matches(listener.identifier):
                matching.append(listener)

        # in case of multiple matching listeners, the most specific should be returned

        def count_populated_attributes(listener_item: Listener):
            return listener_item.identifier.count_populated()

        return max(matching, key=count_populated_attributes, default=None)
