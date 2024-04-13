#HALO INI ADALAH CLONE DARI PYROFORK.

from enum import auto

from .auto_name import AutoName


class PollType(AutoName):
    """Poll type enumeration used in :obj:`~haku.types.Poll`."""

    QUIZ = auto()
    "Quiz poll"

    REGULAR = auto()
    "Regular poll"
