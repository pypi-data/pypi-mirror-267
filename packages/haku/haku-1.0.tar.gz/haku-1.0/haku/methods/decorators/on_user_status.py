#HALO INI ADALAH CLONE DARI PYROFORK.

from typing import Callable

import haku
from haku.filters import Filter


class OnUserStatus:
    def on_user_status(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling user status updates.
        This does the same thing as :meth:`~haku.Client.add_handler` using the
        :obj:`~haku.handlers.UserStatusHandler`.

        Parameters:
            filters (:obj:`~haku.filters`, *optional*):
                Pass one or more filters to allow only a subset of UserStatus updated to be passed in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, haku.Client):
                self.add_handler(haku.handlers.UserStatusHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        haku.handlers.UserStatusHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
