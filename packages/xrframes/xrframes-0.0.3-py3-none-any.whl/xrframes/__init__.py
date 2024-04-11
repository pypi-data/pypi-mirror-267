"""
Similar to ``xmovie``, make animations from xarray objects.
"""

__version__ = "0.0.3"

from .core import Frames
from .util import cleanup

__all__ = (
    "Frames",
    "cleanup",
)
