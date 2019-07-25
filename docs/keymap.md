# Keymap

Keymaps in KMK are simple Python class objects with various attributes assigned
(some by default, however all are overridable).

The basics of what you'll need to get started are:

- Import the `KeyboardConfig` object for your keyboard from `kmk.boards` (or, if
  handwiring your keyboard, import `KeyboardConfig` from the appropriate MCU for your
  board from `kmk.mcus`. See `hardware.md` for the list of supported boards and
  map this to the correct Python module under either of those paths.

- Add a file to `user_keymaps/your_username` called whatever you'd like

- Assign a `KeyboardConfig` instance to a variable (ex. `keyboard = KeyboardConfig()` - note
  the parentheses)

- Make sure this `KeyboardConfig` instance is actually run at the end of the file with
  a block such as the following:

```python
if __name__ == '__main__':
    keyboard.go()
```

- Assign pins and your diode orientation (only necessary on handwire keyboards),
  for example:

```python
col_pins = (P.SCK, P.MOSI, P.MISO, P.RX, P.TX, P.D4)
row_pins = (P.D10, P.D11, P.D12, P.D13, P.D9, P.D6, P.D5, P.SCL)
rollover_cols_every_rows = 4
diode_orientation = DiodeOrientation.COLUMNS

swap_indicies = {
    (3, 3): (3, 9),
    (3, 4): (3, 10),
    (3, 5): (3, 11),
}
```

The pins should be based on whatever CircuitPython calls pins on your particular
board. You can find these in the REPL on your CircuitPython device:

```python
import board
print(dir(board))
```

> Note: `rollover_cols_every_rows` is only supported with
> `DiodeOrientation.COLUMNS`, not `DiodeOrientation.ROWS`. It is used for boards
> such as the Planck Rev6 which reuse column pins to simulate a 4x12 matrix in
> the form of an 8x6 matrix

> Note: `swap_indicies` is used to literally flip two keys' positions in the
> matrix. This is pretty rarely needed, but for example the Planck Rev6 in full
> 1u Grid mode swaps the bottom three right keys on each "half", thus the
> example above

You can further define a bunch of other stuff:

- `debug_enabled` which will spew a ton of debugging information to the serial
  console. This is very rarely needed, but can provide very valuable information
  if you need to open an issue.

- `unicode_mode` from `kmk.consts.UnicodeMode`, which defines the default
  operating system implementation to use for unicode sequences (see examples
  below, or `unicode.md`. This can be changed after boot with a key (see
  `keycodes.md`)

- `tap_time` which defines how long `KC.TT` and `KC.LT` will wait before
  considering a key "held" (see `keycodes.md`)

- `leader_dictionary`, which defines leader sequences (see `leader.md`), defined
  as tuples of keycode objects (or you can use
  `kmk.keycodes.generate_leader_dictionary_seq` with a string)

We also support unicode sequences (emojis, emoticons, umlauted letters,
whatever) if your operating system and system setup do! See `unicode.md` for
details.

Here's a giant example of all the above. This is my personal 4x12 matrix layout
running on a Planck Rev6 PCB, with a Feather M4 Express wired up to the outer
matrix pins (in somewhat of a "spider" setup), utilizing most of the above
features:

```python
from kmk.boards.klarank import KeyboardConfig
from kmk.consts import UnicodeMode
from kmk.keycodes import KC
from kmk.keycodes import generate_leader_dictionary_seq as glds
from kmk.macros.simple import send_string
from kmk.macros.unicode import compile_unicode_string_sequences as cuss

keyboard = KeyboardConfig()

keyboard.debug_enabled = True
keyboard.unicode_mode = UnicodeMode.LINUX

_______ = KC.TRNS
xxxxxxx = KC.NO

emoticons = cuss({
    # Emojis
    'BEER': r'🍺',
    'BEER_TOAST': r'🍻',
    'FACE_CUTE_SMILE': r'😊',
    'FACE_HEART_EYES': r'😍',
    'FACE_JOY': r'😂',
    'FACE_SWEAT_SMILE': r'😅',
    'FACE_THINKING': r'🤔',
    'FIRE': r'🔥',
    'FLAG_CA': r'🇨🇦',
    'FLAG_US': r'🇺🇸',
    'HAND_CLAP': r'👏',
    'HAND_HORNS': r'🤘',
    'HAND_OK': r'👌',
    'HAND_THUMB_DOWN': r'👎',
    'HAND_THUMB_UP': r'👍',
    'HAND_WAVE': r'👋',
    'HEART': r'❤️',
    'MAPLE_LEAF': r'🍁',
    'POOP': r'💩',
    'TADA': r'🎉',

    # Emoticons, but fancier
    'ANGRY_TABLE_FLIP': r'(ノಠ痊ಠ)ノ彡┻━┻',
    'CELEBRATORY_GLITTER': r'+｡:.ﾟヽ(´∀｡)ﾉﾟ.:｡+ﾟﾟ+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟ',
    'SHRUGGIE': r'¯\_(ツ)_/¯',
    'TABLE_FLIP': r'(╯°□°）╯︵ ┻━┻',
})

WPM = send_string("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum arcu vitae elementum curabitur vitae nunc sed. Facilisis sed odio morbi quis.")

keyboard.leader_dictionary = {
    glds('hello'): send_string('hello world from kmk macros'),
    glds('wpm'): WPM,
    glds('atf'): emoticons.ANGRY_TABLE_FLIP,
    glds('tf'): emoticons.TABLE_FLIP,
    glds('fca'): emoticons.FLAG_CA,
    glds('fus'): emoticons.FLAG_US,
    glds('cel'): emoticons.CELEBRATORY_GLITTER,
}

keyboard.keymap = [
    [
        [KC.GESC, KC.QUOT, KC.COMM,            KC.DOT,   KC.P,     KC.Y,    KC.F,    KC.G,     KC.C,    KC.R,    KC.L,  KC.BSPC],
        [KC.TAB,  KC.A,    KC.O,               KC.E,     KC.U,     KC.I,    KC.D,    KC.H,     KC.T,    KC.N,    KC.S,  KC.ENT],
        [KC.LGUI, KC.SCLN, KC.Q,               KC.J,     KC.K,     KC.X,    KC.B,    KC.M,     KC.W,    KC.V,    KC.Z,  KC.LALT],
        [KC.LCTL, KC.LEAD, KC.LSHIFT(KC.LGUI), KC.MO(2), KC.MO(3), KC.LSFT, KC.SPC,  KC.MO(1), KC.LEFT, KC.DOWN, KC.UP, KC.RGHT],
    ],

    [
        [KC.GESC, xxxxxxx, xxxxxxx, KC.F10, KC.F11, KC.F12, xxxxxxx, KC.PSLS, KC.N7, KC.N8,  KC.N9,   KC.BSPC],
        [KC.TAB,  xxxxxxx, xxxxxxx, KC.F7,  KC.F8,  KC.F9,  xxxxxxx, KC.PAST, KC.N4, KC.N5,  KC.N6,   _______],
        [KC.LGUI, xxxxxxx, xxxxxxx, KC.F4,  KC.F5,  KC.F6,  xxxxxxx, KC.PMNS, KC.N1, KC.N2,  KC.N3,   _______],
        [KC.LCTL, xxxxxxx, _______, KC.F1,  KC.F2,  KC.F3,  KC.SPC,  _______, KC.N0, KC.DOT, xxxxxxx, KC.EQL],
    ],

    [
        [KC.GESC, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.BSLS, KC.LBRC, KC.RBRC, KC.DEL],
        [KC.TAB,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.MINS],
        [KC.LGUI, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.LBRC, xxxxxxx, xxxxxxx, KC.INS],
        [KC.LCTL, xxxxxxx, _______, _______, xxxxxxx, _______, xxxxxxx, xxxxxxx, KC.HOME, KC.PGDN, KC.PGUP, KC.END],
    ],

    [
        [KC.GRV,  KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.SLSH],
        [KC.TAB,  xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, KC.MINS],
        [KC.LGUI, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx, xxxxxxx],
        [KC.LCTL, xxxxxxx, xxxxxxx, xxxxxxx, _______, _______, xxxxxxx, xxxxxxx, KC.MUTE, KC.VOLD, KC.VOLU, xxxxxxx],
    ],
]

if __name__ == '__main__':
    keyboard.go()
```
