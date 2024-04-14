# version placeholder (replaced by poetry-dynamic-versioning)
__version__ = "1.1.6.3"

# global app config
from .core import configurator

config = configurator.config

# helpers
from .core import helpers
