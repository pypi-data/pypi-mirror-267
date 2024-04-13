#HALO INI ADALAH CLONE DARI PYROFORK.

from typing import Callable

import haku
from haku.filters import Filter


class OnInlineQuery:
    def on_inline_query(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling inline queries.

        This does the same thing as :meth:`~haku.Client.add_handler` using the
        :obj:`~haku.handlers.InlineQueryHandler`.

        Parameters:
            filters (:obj:`~haku.filters`, *optional*):
                Pass one or more filters to allow only a subset of inline queries to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, haku.Client):
                self.add_handler(haku.handlers.InlineQueryHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        haku.handlers.InlineQueryHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
