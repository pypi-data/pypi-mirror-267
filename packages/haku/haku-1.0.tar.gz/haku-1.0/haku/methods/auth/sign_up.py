#HALO INI ADALAH CLONE DARI PYROFORK.

import logging

import haku
from haku import raw
from haku import types

log = logging.getLogger(__name__)


class SignUp:
    async def sign_up(
        self: "haku.Client",
        phone_number: str,
        phone_code_hash: str,
        first_name: str,
        last_name: str = ""
    ) -> "types.User":
        """Register a new user in Telegram.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Code identifier taken from the result of :meth:`~haku.Client.send_code`.

            first_name (``str``):
                New user first name.

            last_name (``str``, *optional*):
                New user last name. Defaults to "" (empty string, no last name).

        Returns:
            :obj:`~haku.types.User`: On success, the new registered user is returned.

        Raises:
            BadRequest: In case the arguments are invalid.
        """
        phone_number = phone_number.strip(" +")

        r = await self.invoke(
            raw.functions.auth.SignUp(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                phone_code_hash=phone_code_hash
            )
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
