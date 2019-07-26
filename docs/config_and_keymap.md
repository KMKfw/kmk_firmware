# Configuring KMK

KMK is configured through a rather large plain-old-Python class called
`KMKKeyboard`. Subclasses of this configuration exist which pre-fill defaults
for various known keyboards (for example, many Keebio keyboards are supported
through our ItsyBitsy to ProMicro pinout adapter). This class is the main
interface between end users and the inner workings of KMK. Let's dive in!

- Edit or create a file called `main.py` on your `CIRCUITPY` drive. You can also
  keep this file on your computer (perhaps under `user_keymaps` - please feel
  free to submit a pull request with your layout definitions!) and copy it over
  (either manually or, if you're adept with developer tooling and/or a command
  line, [our
  Makefile](https://github.com/KMKfw/kmk_firmware/blob/master/docs/flashing.md)).
  It's definitely recommended to keep a backup of your configuration somewhere
  that isn't the microcontroller itself - MCUs die, CircuitPython may run into
  corruption bugs, or you might just have bad luck and delete the wrong file
  some day.

- Import the `KMKKeyboard` object for your keyboard from `kmk.boards` (or, if
  handwiring your keyboard, import `KMKKeyboard` from `kmk.kmk_keyboard`).

- Assign a `KMKKeyboard` instance to a variable (ex. `keyboard = KMKKeyboard()` - note
  the parentheses)

- Make sure this `KMKKeyboard` instance is actually run at the end of the file with
  a block such as the following:

```python
if __name__ == '__main__':
    keyboard.go()
```

- Assign pins and your diode orientation (only necessary on handwire keyboards),
  for example:

```python
import board

from kmk.matrix import DiodeOrientation

col_pins = (board.SCK, board.MOSI, board.MISO, board.RX, board.TX, board.D4)
row_pins = (board.D10, board.D11, board.D12, board.D13, board.D9, board.D6, board.D5, board.SCL)
rollover_cols_every_rows = 4
diode_orientation = DiodeOrientation.COLUMNS
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

- Import the global list of key definitions with `from kmk.keys import KC`. You
  can either print this out in the REPL as we did with `board` above, or simply
  look at [our Key
  documentation](https://github.com/KMKfw/kmk_firmware/blob/master/docs/keycodes.md).
  We've tried to keep that listing reasonably up to date, but if it feels like
  something is missing, you may need to read through `kmk/keys.py` (and then
  open a ticket to tell us our docs are out of date, or open a PR and fix the
  docs yourself!)

- Define a keymap, which is, in Python terms, a List of Lists of `Key` objects.
  A very simple keymap, for a keyboard with just two physical keys on a single
  layer, may look like this:

```python
keyboard.keymap = [[KC.A, KC.B]]
```

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

[Here's a giant example of all the
above](https://github.com/KMKfw/kmk_firmware/blob/master/user_keymaps/klardotsh/klarank_featherm4.py).
This is my personal 4x12 matrix layout running on a Planck Rev6 PCB, with a
Feather M4 Express wired up to the outer matrix pins (in somewhat of a "spider"
setup), utilizing most of the above features - it's one of the "kitchen sink
tester" definitions we use on the KMK Core team.
