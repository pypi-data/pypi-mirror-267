#HALO INI ADALAH CLONE DARI PYROFORK.

import haku
from haku import raw, types


class DeleteBotCommands:
    async def delete_bot_commands(
        self: "haku.Client",
        scope: "types.BotCommandScope" = types.BotCommandScopeDefault(),
        language_code: str = "",
    ) -> bool:
        """Delete the list of the bot's commands for the given scope and user language.
        After deletion, higher level commands will be shown to affected users.

        The commands passed will overwrite any command set previously.
        This method can be used by the own bot only.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            scope (:obj:`~haku.types.BotCommandScope`, *optional*):
                An object describing the scope of users for which the commands are relevant.
                Defaults to :obj:`~haku.types.BotCommandScopeDefault`.

            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code.
                If empty, commands will be applied to all users from the given scope, for whose language there are no
                dedicated commands.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Delete commands
                await app.delete_bot_commands()
        """

        return await self.invoke(
            raw.functions.bots.ResetBotCommands(
                scope=await scope.write(self),
                lang_code=language_code,
            )
        )
