#HALO INI ADALAH CLONE DARI PYROFORK.

import logging
from typing import List

import haku
from haku import raw
from haku import types

log = logging.getLogger(__name__)


class GetContacts:
    async def get_contacts(
        self: "haku.Client"
    ) -> List["types.User"]:
        """Get contacts from your Telegram address book.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~haku.types.User`: On success, a list of users is returned.

        Example:
            .. code-block:: python

                contacts = await app.get_contacts()
                print(contacts)
        """
        contacts = await self.invoke(raw.functions.contacts.GetContacts(hash=0))
        return types.List(types.User._parse(self, user) for user in contacts.users)
