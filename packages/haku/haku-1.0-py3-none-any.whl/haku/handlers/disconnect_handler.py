#HALO INI ADALAH CLONE DARI PYROFORK.

from typing import Callable

from .handler import Handler


class DisconnectHandler(Handler):
    """The Disconnect handler class. Used to handle disconnections. It is intended to be used with
    :meth:`~haku.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~haku.Client.on_disconnect` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a disconnection occurs. It takes *(client)*
            as positional argument (look at the section below for a detailed description).

    Other parameters:
        client (:obj:`~haku.Client`):
            The Client itself. Useful, for example, when you want to change the proxy before a new connection
            is established.
    """

    def __init__(self, callback: Callable):
        super().__init__(callback)
