# flake8: noqa
import sys
import pkg_resources

pyversion = float(sys.version[:3])
if pyversion < 3.6:
    sys.exit('fast-autocomplete requires Python 3.6 or later.')

# __version__ = pkg_resources.get_distribution("fast-autocomplete").version

from .dwg import AutoComplete
from .draw import DrawGraphMixin
from .demo import demo
from .loader import autocomplete_factory
from .normalize import Normalizer
