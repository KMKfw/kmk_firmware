# Keys

**Note:** This is not a lookup table of key objects provided by KMK. That listing
can be found in [`keycodes.md`](keycodes.md). It's probably worth a look at the raw source if
you're stumped: [`kmk/keys.py`](/kmk/keys.py).

---

## Key Objects

This is a bunch of documentation about how a physical keypress translates to
events (and the lifecycle of said events) in KMK. It's somewhat technical, but
if you're looking to extend your keyboard's functionality with extra code,
you'll need at least some of this technical knowledge.

The first few steps in the process aren't all that interesting for most
workflows, which is why they're buried deep in KMK: we scan a bunch of GPIO
lanes (about as quickly as CircuitPython will let us) to see where, in a matrix
of keys, a key has been pressed. The technical details about this process [are
probably best left to
Wikipedia](https://en.wikipedia.org/wiki/Keyboard_matrix_circuit). Then, we scan
through the defined keymap, finding the first valid key at this index based on
the stack of currently active layers (this logic, if you want to read through
the code, is in [`kmk/kmk_keyboard.py`](/kmk/kmk_keyboard.py), method `_find_key_in_map`).

The next few steps are the interesting part, but to understand them, we need to
understand a bit about what a `Key` object is (found in [`kmk/keys.py`](/kmk/keys.py)). `Key`
objects have a few core pieces of information:

- Their `code`, which can be any integer or None. Integers sent through to the
  HID stack (and thus the computer, which will translate that integer to
  something meaningful - for example, `code=4` becomes `a` on a US QWERTY/Dvorak
  keyboard).

- Handlers for "press" (sometimes known as "keydown") and "release" (sometimes
  known as "keyup") events. KMK provides handlers for standard keyboard
  functions and some special override keys (like `KC.GESC`, which is an enhanced
  form of existing ANSI keys) in [`kmk/handlers/stock.py`](/kmk/handlers/stock.py).

- A generic `meta` field, which is most commonly used for "argumented" keys -
  objects in the `KC` object which are actually functions that return `Key`
  instances, which often need to access the arguments passed into the "outer"
  function. Many of these examples are related to layer switching - for example,
  `KC.MO` is implemented as an argumented key - when the user adds `KC.MO(1)` to
  their keymap, the function call returns a `Key` object with `meta` set to an
  object containing `layer` and `kc` properties, for example. There's other uses
  for `meta`, and examples can be found in [`kmk/types.py`](/kmk/types.py)

`Key` objects can also be chained together by calling them! To create a key
which holds Control and Shift simultaneously, we can simply do:

```python
CTRLSHFT = KC.LCTL(KC.LSFT)

keyboard.keymap = [ ... CTRLSHFT ... ]
```

When a key is pressed and we've pulled a `Key` object out of the keymap, the
`Key` is first passed through the module processing pipeline.
Modules can do whatever with that `Key`, but usually keys either pass right
through, or are intercepted and emitted again later (think of timing based
modules like Combos and Hold-Tap).
Finally the assigned press handler will be run (most commonly, this is provided
by KMK).
On release the `Key` object lookup is, most of the time, cached and doesn't
require searching the keymap again.
Then it's the processing pipeline again, followed by the release handler.

Custom behavior can either be achieved with custom press and release handlers or
with [macros](docs/en/macros.md).

## The Key Code Dictionary

You can also refer to a key by index:

- `KC['A']`
- `KC['NO']`
- `KC['LALT']`

Or the `KC.get` function which has an optional default argument, which will
be returned if the key is not found (`default=None` unless otherwise specified):

- `KC.get('A')`
- `KC.get('NO', None)`
- `KC.get('NOT DEFINED', KC.RALT)`

Key names are case-sensitive. `KC['NO']` is different from `KC['no']`. It is recommended
that names are normally UPPER_CASE. The exception to this are alpha keys; `KC['A']` and
`KC['a']` will both return the same, unshifted, key.
