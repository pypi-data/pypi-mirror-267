#HALO INI ADALAH CLONE DARI PYROFORK.

import inspect
import haku

from haku.errors import ListenerStopped
from haku.types import Listener
from haku.utils import PyromodConfig

class StopListener:
    async def stop_listener(
        self: "haku.Client",
        listener: Listener
    ):
        """Stops a listener, calling stopped_handler if applicable or raising ListenerStopped if throw_exceptions is True.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            listener (:obj:`~haku.types.Listener`):
                The listener to remove.

        Raises:
            ListenerStopped: If throw_exceptions is True.
        """
        self.remove_listener(listener)

        if listener.future.done():
            return

        if callable(PyromodConfig.stopped_handler):
            if inspect.iscoroutinefunction(PyromodConfig.stopped_handler.__call__):
                await PyromodConfig.stopped_handler(None, listener)
            else:
                await self.loop.run_in_executor(
                    None, PyromodConfig.stopped_handler, None, listener
                )
        elif PyromodConfig.throw_exceptions:
            listener.future.set_exception(ListenerStopped())
