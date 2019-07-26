# Welcome to RAM and stack size hacks central, I'm your host, klardotsh!
# Our import structure is deeply nested enough that stuff
# breaks in some truly bizarre ways, including:
# - explicit RuntimeError exceptions, complaining that our
#   stack depth is too deep
#
# - silent hard locks of the device (basically unrecoverable without
#   UF2 flash if done in main.py, fixable with a reboot if done
#   in REPL)
#
# However, there's a hackaround that works for us! Because sys.modules
# caches everything it sees (and future imports will use that cached
# copy of the module), let's take this opportunity _way_ up the import
# chain to import _every single thing_ KMK eventually uses in a normal
# workflow, in nesting order
#
# GC runs automatically after CircuitPython imports.

# First, system-provided deps
import busio
import collections
import gc
import supervisor

# Now "light" KMK stuff with few/no external deps
import kmk.consts  # isort:skip
import kmk.kmktime  # isort:skip
import kmk.types  # isort:skip

from kmk.consts import LeaderMode, UnicodeMode, KMK_RELEASE  # isort:skip
from kmk.hid import USBHID  # isort:skip
from kmk.internal_state import InternalState  # isort:skip
from kmk.keys import KC  # isort:skip
from kmk.matrix import MatrixScanner  # isort:skip

# Now handlers that will be used in keys later
import kmk.handlers.layers  # isort:skip
import kmk.handlers.stock  # isort:skip

# Now stuff that depends on the above (and so on)
import kmk.keys  # isort:skip
import kmk.matrix  # isort:skip

import kmk.hid  # isort:skip
import kmk.internal_state  # isort:skip
