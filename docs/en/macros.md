# Macros

Macros are used for sending multiple keystrokes in a single action, and can
be used for things like Unicode characters (even emojis! 🇨🇦), _Lorem ipsum_
generators, triggering side effects (think lighting, speakers,
microcontroller-optimized cryptocurrency miners, whatever).
Macros have worse performance and higher memory usage than [custom keys](keys.md),
so unless the objective is to type out a sequence or to perform an action repeatedly
and asynchronously while a key is pressed, custom keys are the recommended solution.

## Setup

```python
from kmk.modules.macros import Macros

macros = Macros()
keyboard.modules.append(macros)
```

This will enable a new type of keycode: `KC.MACRO()`

## Keycodes

|Key                |Description                               |
|-------------------|------------------------------------------|
|`KC.MACRO(macro)`  |Create a key that will play back a macro. |
|`KC.UC_MODE_IBUS`  |Switch Unicode mode to IBus.              |
|`KC.UC_MODE_MACOS` |Switch Unicode mode to macOS.             |
|`KC.UC_MODE_WINC`  |Switch Unicode mode to Windows Compose.   |

Full macro signature, all arguments optional:

```python
KC.MACRO(
    on_press=None,
    on_hold=None,
    on_release=None,
    blocking=True,
)
```

### `on_press`
This sequence is run once at the beginning, just after the macro key has been
pressed.
`KC.MACRO(macro)` is actually a short-hand for `KC.MACRO(on_press=macro)`.

### `on_hold`
This sequence is run in a loop while the macro key is pressed (or "held").
If the key is released before the `on_press` sequence is finished, the `on_hold`
sequence will be skipped.

### `on_release`
This sequence is run once at the end, after the macro key has been released and
the previous sequence has finished.

### `blocking`
By default, all key events will be intercepted while a macro is running and
replayed after all blocking macros have finished.
This is to avoid side effects and can be disabled with `blocking=False` if
undesired.
(And yes, technically multiple blocking macros can run simultaneously, the
achievement of which is left as an exercise to the reader.)

## Sending strings

The most basic sequence is an ASCII string. It can be used to send any standard
English alphabet character, and an assortment of other "standard" keyboard keys
(return, space, exclamation points, etc.).
Keep in mind that some characters from shifted keys are i18n dependent.

```python
WOW = KC.MACRO("Wow, KMK is awesome!")

keyboard.keymap = [<other keycodes>, WOW, <other keycodes>]
```

## Key sequences

If you need to add modifier keys to your sequence or you need more granular control.
You can use it to add things like copying/pasting, tabbing between fields, etc.

```python
from kmk.modules.macros import Press, Release, Tap

PASTE_WITH_COMMENTARY = KC.MACRO(
    "look at this: ",
    Press(KC.LCTL),
    Tap(KC.V),
    Release(KC.LCTL)
)

keyboard.keymap = [<other keycodes>, PASTE_WITH_COMMENTARY, <other keycodes>]
```

The above example will type out "look at this: " and then paste the contents of your
clipboard.


### Sleeping within a sequence

If you need to wait during a sequence, you can use `Delay(ms)` to wait a
length of time, in milliseconds.

```python
from kmk.modules.macros import Tap, Delay

COUNTDOWN_TO_PASTE = KC.MACRO(
    Tap(KC.N3),
    Tap(KC.ENTER),
    Delay(1000),
    Tap(KC.N2),
    Tap(KC.ENTER),
    Delay(1000),
    Tap(KC.N1),
    Tap(KC.ENTER),
    Delay(1000),
    Tap(KC.LCTL(KC.V)),
)

keyboard.keymap = [<other keycodes>, COUNTDOWN_TO_PASTE, <other keycodes>]
```

This example will type out the following, waiting one second (1000 ms) between numbers:

    3
    2
    1

and then paste the contents of your clipboard.

### Alt Tab with delay

If alt tab isn't working because it requires a delay, adding a delay and triggering
down and up on ALT manually may fix the issue.

``` python
from kmk.modules.macros import Delay, Press, Release, Tap

NEXT = KC.MACRO(
    Press(KC.LALT),
    Delay(30),
    Tap(KC.TAB),
    Delay(30),
    Release(KC.LALT),
)
```

## Unicode

### Unicode Modes

On Linux, Unicode uses `Ctrl-Shift-U`, which is supported by `ibus` and GTK+3.
`ibus` users will need to add `IBUS_ENABLE_CTRL_SHIFT_U=1` to their environment
(`~/profile`, `~/.bashrc`, `~/.zshrc`, or through your desktop environment's
configurator).

On Windows, [WinCompose](https://github.com/samhocevar/wincompose) is required.

- Linux : `UnicodeModeIBus`, the default
- MacOS: `UnicodeModeMacOS`
- Windows: `UnicodeModeWinC`

### Unicode Examples

Initialize `Macros` to use `UnicodeModeMac` and make a key to cycle between modes
at runtime.

```python
from kmk.keys import Key
from kmk.modules.macros import Macros, UnicodeModeIBus, UnicodeModeMacOS, UnicodeModeWinC

macros = Macros(unicode_mode=UnicodeModeMacOS)
keyboard.modules.append(macros)

def switch_um(keyboard):
    if macros.unicode_mode == UnicodeModeIBus:
        macros.unicode_mode = UnicodeModeMacOS
    elif macros.unicode_mode == UnicodeModeMacOS:
        macros.unicode_mode = UnicodeModeWinC
    else:
        macros.Unicode_mode = UnicodeModeIBus

UCCYCLE = Key(code=None, on_press=switch_um)

FLIP = KC.MACRO('(ノಠ痊ಠ)ノ彡┻━┻')

keyboard.keymap = [<other keycodes>, UCCYCLE, FLIP, <other keycodes>]
```

## Arbitrary Actions

As it happens, macros accept any callable object (even generators) as arguments.
The `KMKKeyboard` object is passed as argument to that callable.

### Example 1

Change the RGB animation mode to "SWIRL" for five seconds and print an ASCII
spinner

```python
# ... boilerplate omitted for brevity.

prev_animation = None

def start_spinning(keyboard):
    global prev_animation
    prev_animation = rgb.animation_mode
    rgb.animation_mode = AnimationModes.SWIRL
    rgb.effect_init = True

def stop_spinning(keyboard):
    rgb.animation_mode = prev_animation
    rgb.effect_init = True

DISCO = KC.MACRO(
    "disco time!",
    start_color_wheel,
    "-",
    DELAY(1000),
    KC.BSPC,
    "\\",
    DELAY(1000),
    KC.BSPC,
    "|",
    DELAY(1000),
    KC.BSPC,
    "/",
    DELAY(1000),
    KC.BSPC,
    "-",
    DELAY(1000),
    KC.BSPC,
    stop_color_wheel,
    " disco time over.",
    )
```

### Example 2a

Here's a programmatic version of the earlier countdown-to-paste example, using a
generator.
Any integer return value is interpreted as a delay instruction in milliseconds.

```python
def countdown(count, delay_ms):
    def generator(keyboard):
        for n in range(count, 0, -1):
            KC[n].on_press(keyboard)
            yield
            KC[n].on_release(keyboard)
            yield
            KC.ENTER.on_press(keyboard)
            yield
            KC.ENTER.on_release(keyboard)
            yield delay_ms
    return generator

COUNTDOWN_TO_PASTE = KC.MACRO(
    countdown(3, 1000),
    Tap(KC.LCTL(KC.V)),
)
```

### Example 2b

On popular demand: Callables in macros are fully recursive.
Here's a programmatic version of the earlier countdown example, using a
generator, but the countdown gets faster and there's a surprise at the end

```python
def countdown(count, delay_ms):
    def generator(keyboard):
        for n in range(count, 0, -1):
            yield '{n}\n'.format(n)
            yield n * delay_ms
        yield '#🎉; open https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/macros.md'
    return generator

COUNTDOWN_TO_SURPRISE = KC.MACRO(
    countdown(10, 100),
)
```

### Example 3

Sometimes there's no need for a generator and a simple function is enough to
type a string that's created at runtime.
And sometimes it's really hard to remember what keys are currently pressed:

```python
def keys_pressed(keyboard):
    return str(keyboard.keys_pressed)

KEYS_PRESSED = KC.MACRO(keys_pressed)
```

### Example 4

A high productivity replacement for the common space key:
This macro ensures that you make good use of your time by measuring how long
you've been holding the space key for, printing the result to the debug
console, all the while reminding you that you're still holding the space key.

```python
from supervisor import ticks_ms
from kmk.utils import Debug

debug = Debug(__name__)

def make_timer():
    ticks = 0
    def _():
        nonlocal ticks
        return (ticks := ticks_ms() - ticks)
    return _

space_timer = make_timer()

SPACETIME = KC.MACRO(
    on_press=(
        lambda _: space_timer() and None,
        Press(KC.SPACE),
        lambda _: debug('start holding space...'),
    ),
    on_hold=(
        lambda _: debug('..still holding space..'),
    ),
    on_release=(
        Release(KC.SPACE),
        lambda _: debug('...end holding space after ', space_timer(), 'ms'),
    ),
    blocking=False,
)
```
