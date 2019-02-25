# Sequences

Sequences are used for sending multiple keystrokes in a single action, and can
be used for things like unicode characters (even emojis! 🇨🇦), lorei epsum
generators, triggering side effects (think lighting, speakers,
microcontroller-optimized cryptocurrency miners, whatever). If you are still
unsure of what this is, most other vendors call these "Macros", but can do much
more if you wish.

## Sending strings
The most basic sequence is `send_string`. It can be used to send any standard
English alphabet character, and an assortment of other "standard" keyboard keys
(return, space, exclamation points, etc.)

```python
from kmk.handlers.sequences import send_string

WOW = send_string("Wow, KMK is awesome!")

keyboard.keymap = [...WOW,...]
```

## Unicode
Before trying to send Unicode sequences, make sure you set your `UnicodeMode`.
You can set an initial value in your keymap by setting `keyboard.unicode_mode`.

Keys are provided to change this mode at runtime - for example, `KC.UC_MODE_LINUX`.


### Unicode Modes:
On Linux, Unicode uses `Ctrl-Shift-U`, which is supported by `ibus` and GTK+3.
`ibus` users will need to add `IBUS_ENABLE_CTRL_SHIFT_U=1` to their environment
(`~/profile`, `~/.bashrc`, `~/.zshrc`, or through your desktop environment's
configurator).

On Windows, [WinCompose](https://github.com/samhocevar/wincompose) is required.

- Linux : `UnicodeMode.LINUX` or `UnicodeMode.IBUS`
- Mac: `UnicodeMode.MACOS` or `UnicodeMode.OSX` or `UnicodeMode.RALT`
- Windows: `UnicodeMode.WINC`


### Unicode Examples

To send a simple unicode symbol
```python
from kmk.handlers.sequences import unicode_string_sequence

FLIP = unicode_string_sequence('(ノಠ痊ಠ)ノ彡┻━┻')

keyboard.keymap = [...FLIP,...]
```

If you'd rather keep a lookup table of your sequences (perhaps to bind emojis to
keys), that's supported too, through an obnoxiously long-winded method:

```python
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss

emoticons = cuss({
	'BEER': r'🍺',
	'HAND_WAVE': r'👋',
})

keymap = [...emoticons.BEER, emoticons.HAND_WAVE...]
```

> The observant will notice dot-notation is supported here despite feeding in a
> dictionary - the return of `compile_unicode_string_sequences` is a
> `kmk.types.AttrDict`, which you can think of as a read-only view over a
> dictionary adding attribute-based (dot-notation) access.

Remember from the Leader Mode documentation that leader sequences simply bind to
keys, so extrapolating this example out a bit, you can bind emojis to leader
sequences matching some name or mnemonic representing the sequence you're
looking to send. If you ever wanted to type `<Leader>fire` and see a fire emoji
on your screen, welcome home.

```python
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss

emoticons = cuss({
    # Emojis
    'BEER': r'🍺',
    'BEER_TOAST': r'🍻',
    'FACE_THINKING': r'🤔',
    'FIRE': r'🔥',
    'FLAG_CA': r'🇨🇦',
    'FLAG_US': r'🇺🇸',
})

keyboard.leader_dictionary = {
    'beer': emoticons.BEER,
    'beers': emoticons.BEER_TOAST,
    'fire': emoticons.FIRE,
    'uhh': emoticons.FACE_THINKING,
    'fca': emoticons.FLAG_CA,
    'fus': emoticons.FLAG_US,
}
```

Finally, if you need to send arbitrary unicode codepoints in raw form, that's
supported too, through `unicode_codepoint_sequence`.

```python
from kmk.handlers.sequences import unicode_codepoint_sequence

TABLE_FLIP = unicode_codepoint_sequence([
	"28", "30ce", "ca0", "75ca","ca0", "29",
	"30ce", "5f61", "253b", "2501", "253b",
])

keyboard.keymap = [...TABLE_FLIP,...]
```
