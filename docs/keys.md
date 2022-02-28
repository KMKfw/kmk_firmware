# Keys

> NOTE: This is not a lookup table of key objects provided by KMK. That listing
> can be found in `keycodes.md`. It's probably worth a look at the raw source if
> you're stumped: `kmk/keys.py`.

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
the code, is in `kmk/internal_state.py`, method `_find_key_in_map`).

The next few steps are the interesting part, but to understand them, we need to
understand a bit about what a `Key` object is (found in `kmk/keys.py`). `Key`
objects have a few core pieces of information:

* Their `code`, which can be any integer. Integers below
  `FIRST_KMK_INTERNAL_KEY` are sent through to the HID stack (and thus the
  computer, which will translate that integer to something meaningful - for
  example, `code=4` becomes `a` on a US QWERTY/Dvorak keyboard).

* Their attached modifiers (to implement things like shifted keys or `KC.HYPR`,
  which are single key presses sending along more than one key in a single HID
  report. This is a distinct concept from Sequences, which are a KMK feature
  documented in `sequences.md`). For almost all purposes outside of KMK core,
  this field should be ignored - it can be safely populated through far more
  sane means than futzing with it by hand.

* Some data on whether the key should actually be pressed or released - this is
  mostly an implementation detail of how Sequences work, where, for example,
  `KC.RALT` may need to be held down for the entirety of a sequence, rather than
  being released immediately before moving to the next character.  Usually end
  users shouldn't need to mess with this, but the fields are called `no_press`
  and `no_release` and are referenced in a few places in the codebase if you
  need examples.

* Handlers for "press" (sometimes known as "keydown") and "release" (sometimes
  known as "keyup") events. KMK provides handlers for standard keyboard
  functions and some special override keys (like `KC.GESC`, which is an enhanced
  form of existing ANSI keys) in `kmk/handlers/stock.py`, for layer switching in
  `kmk/handlers.layers.py`, and for everything related to Sequences (see
  `sequences.md` again) in `kmk/handlers/sequences.py`. We'll discuss these more
  shortly.

* Optional callbacks to be run before and/or after the above handlers. More on
  that soon.

* A generic `meta` field, which is most commonly used for "argumented" keys -
  objects in the `KC` object which are actually functions that return `Key`
  instances, which often need to access the arguments passed into the "outer"
  function. Many of these examples are related to layer switching - for example,
  `KC.MO` is implemented as an argumented key - when the user adds `KC.MO(1)` to
  their keymap, the function call returns a `Key` object with `meta` set to an
  object containing `layer` and `kc` properties, for example. There's other uses
  for `meta`, and examples can be found in `kmk/types.py`

`Key` objects can also be chained together by calling them! To create a key
which holds Control and Shift simultaneously, we can simply do:

```python
CTRLSHFT = KC.LCTL(KC.LSFT)

keyboard.keymap = [ ... CTRLSHFT ... ]
```

When a key is pressed and we've pulled a `Key` object out of the keymap, the
following will happen:

- Pre-press callbacks will be run in the order they were assigned, with their
  return values discarded (unless the user attached these, they will almost
  never exist)
- The assigned press handler will be run (most commonly, this is provided by
  KMK)
- Post-press callbacks will be run in the order they were assigned, with their
  return values discarded (unless the user attached these, they will almost
  never exist)

These same steps are run for when a key is released.

_So now... what's a handler, and what's a pre/post callback?!_

All of these serve rougly the same purpose: to _do something_ with the key's
data, or to fire off side effects. Most handlers are provided by KMK internally
and modify the `InternalState` in some way - adding the key to the HID queue,
changing layers, etc. The pre/post handlers are designed to allow functionality
to be bolted on at these points in the event flow without having to reimplement
(or import and manually call) the internal handlers.

All of these methods take the same arguments, and for this, I'll lift a
docstring straight out of the source:

> Receives the following:
> 
> - self (this Key instance)
> - state (the current InternalState)
> - KC (the global KC lookup table, for convenience)
> - `coord_int` (an internal integer representation of the matrix coordinate
>   for the pressed key - this is likely not useful to end users, but is
>   provided for consistency with the internal handlers)
> - `coord_raw` (an X,Y tuple of the matrix coordinate - also likely not useful)
> 
> The return value of the provided callback is discarded. Exceptions are _not_
> caught, and will likely crash KMK if not handled within your function.
> 
> These handlers are run in attachment order: handlers provided by earlier
> calls of this method will be executed before those provided by later calls.

This means if you want to add things like underglow/LED support, or have a
button that triggers your GSM modem to call someone, or whatever else you can
hack up in CircuitPython, which also retaining layer-switching abilities or
whatever the stock handler is, you're covered. This also means you can add
completely new functionality to KMK by writing your own handler.

Here's an example of an after_press_handler to change the RGB lights with a layer change:
```python
LOWER = KC.DF(LYR_LOWER) #Set layer to LOWER

def low_lights(key, keyboard, *args):
    print('Lower Layer') #serial feedback
    keyboard.pixels.set_hsv_fill(0, 100, 255) #RGB extension call to set (H,S,V) values

LOWER.after_press_handler(low_lights) #call the key with the after_press_handler
```
Here's an example of a lifecycle hook to print a giant Shrek ASCII art. It
doesn't care about any of the arguments passed into it, because it has no
intentions of modifying the internal state. It is purely a [side
effect](https://en.wikipedia.org/wiki/Side_effect_(computer_science)) run every
time Left Alt is pressed:

```python
def shrek(*args, **kwargs):
    print('⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆')
    print('⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿')
    print('⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀')
    print('⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉')
    
    return False #Returning True will follow thru the normal handlers sending the ALT key to the OS
KC.LALT.before_press_handler(shrek)
```

You can also copy a key without any pre/post handlers attached with `.clone()`,
so for example, if I've already added Shrek to my `LALT` but want a Shrek-less
`LALT` key elsewhere in my keymap, I can just clone it, and the new key won't
have my handlers attached:

```python
SHREKLESS_ALT = KC.LALT.clone()
```
