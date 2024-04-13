#HALO INI ADALAH CLONE DARI PYROFORK.

from enum import auto
from .auto_name import AutoName


class ReactionType(AutoName):
    """Reaction type enumeration used in :obj:`~haku.types.ReactionType`."""
    EMOJI = auto()
    """Emoji reaction type."""

    CUSTOM_EMOJI = auto()
    """Custom emoji reaction type."""
