#!/usr/bin/env micropython

import sys

import uos

from kmk.common.keycodes import Keycodes, RawKeycodes

if len(sys.argv) < 2:
    print('Must provide a keymap to test as first argument', file=sys.stderr)
    sys.exit(200)

user_keymap_file = sys.argv[1]

if user_keymap_file.endswith('.py'):
    user_keymap_file = user_keymap_file[:-3]

# Before we can import the user's keymap, we need to wrangle sys.path to
# add our stub modules. Before we can do THAT, we have to figure out where
# we actually are, and that's not the most trivial thing in MicroPython!
#
# The hack here is to see if we can find ourselves in whatever uPy thinks
# the current directory is. If we can, we need to head up a level. Obviously,
# if the layout of the KMK repo ever changes, this script will need updated
# or all hell will break loose.

# First, hack around https://github.com/micropython/micropython/issues/2322,
# where frozen modules aren't available if MicroPython is running a script
# rather than via REPL
sys.path.insert(0, '')

if any(fname == 'keymap_sanity_check.py' for fname, _, _ in uos.ilistdir()):
    sys.path.extend(('../', '../upy-unix-stubs/'))
else:
    sys.path.extend(('./', './upy-unix-stubs'))

user_keymap = __import__(user_keymap_file)

if hasattr(user_keymap, 'cols') or hasattr(user_keymap, 'rows'):
    assert hasattr(user_keymap, 'cols'), 'Handwired keyboards must have both rows and cols defined'
    assert hasattr(user_keymap, 'rows'), 'Handwired keyboards must have both rows and cols defined'

    # Ensure that no pins are duplicated in a handwire config
    # This is the same check done in the MatrixScanners, relying
    # on the __repr__ of the objects to be unique (because generally,
    # Pin objects themselves are not hashable)
    assert len(user_keymap.cols) == len({p for p in user_keymap.cols}), \
        'Cannot use a single pin for multiple columns'
    assert len(user_keymap.rows) == len({p for p in user_keymap.rows}), \
        'Cannot use a single pin for multiple rows'

    unique_pins = {repr(c) for c in user_keymap.cols} | {repr(r) for r in user_keymap.rows}
    assert len(unique_pins) == len(user_keymap.cols) + len(user_keymap.rows), \
        'Cannot use a pin as both a column and row'

assert hasattr(user_keymap, 'keymap'), 'Must define a keymap array'
assert len(user_keymap.keymap), 'Keymap must contain at least one layer'

for lidx, layer in enumerate(user_keymap.keymap):
    assert len(layer), 'Layer {} must contain at least one row'.format(lidx)
    assert all(len(row) for row in layer), 'Layer {} must not contain empty rows'.format(lidx)
    assert all(len(row) == len(layer[0]) for row in user_keymap.keymap), \
        'All rows in layer {} must be of the same length'.format(lidx)

    for ridx, row in enumerate(layer):
        for cidx, key in enumerate(row):
            if key.code == RawKeycodes.KC_MO:
                assert user_keymap.keymap[key.layer][ridx][cidx] == Keycodes.KMK.KC_TRNS, \
                    ('The physical key used for MO layer switching must be KC_TRNS on the '
                     'target layer or you will get stuck on that layer.')
