#HALO INI ADALAH CLONE DARI PYROFORK.

from typing import Callable

import haku


class OnDisconnect:
    def on_disconnect(self=None) -> Callable:
        """Decorator for handling disconnections.

        This does the same thing as :meth:`~haku.Client.add_handler` using the
        :obj:`~haku.handlers.DisconnectHandler`.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, haku.Client):
                self.add_handler(haku.handlers.DisconnectHandler(func))
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append((haku.handlers.DisconnectHandler(func), 0))

            return func

        return decorator
