#HALO INI ADALAH CLONE DARI PYROFORK.

import asyncio
import inspect

import haku
from haku.methods.utilities.idle import idle


class Run:
    def run(
        self: "haku.Client",
        coroutine=None
    ):
        """Start the client, idle the main script and finally stop the client.

        When calling this method without any argument it acts as a convenience method that calls
        :meth:`~haku.Client.start`, :meth:`~haku.idle` and :meth:`~haku.Client.stop` in sequence.
        It makes running a single client less verbose.

        In case a coroutine is passed as argument, runs the coroutine until it's completed and doesn't do any client
        operation. This is almost the same as :py:obj:`asyncio.run` except for the fact that Haku's ``run`` uses the
        current event loop instead of a new one.

        If you want to run multiple clients at once, see :meth:`haku.compose`.

        Parameters:
            coroutine (``Coroutine``, *optional*):
                Pass a coroutine to run it until it completes.

        Raises:
            ConnectionError: In case you try to run an already started client.

        Example:
            .. code-block:: python

                from haku import Client

                app = Client("my_account")
                ...  # Set handlers up
                app.run()

            .. code-block:: python

                from haku import Client

                app = Client("my_account")


                async def main():
                    async with app:
                        print(await app.get_me())


                app.run(main())
        """
        loop = asyncio.get_event_loop()
        run = loop.run_until_complete

        if coroutine is not None:
            run(coroutine)
        else:
            if inspect.iscoroutinefunction(self.start):
                run(self.start())
                run(idle())
                run(self.stop())
            else:
                self.start()
                run(idle())
                self.stop()
