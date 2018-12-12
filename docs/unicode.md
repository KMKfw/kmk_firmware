# Macros And Unicode
Macros are used for sending multiple keystrokes in a single action. This is useful for
things like unicode input, sending strings of text, or other automation.

## Basic Macros
The most basic macro is send_string(). It can be used to send any standard ASCII keycode, including the return and tab key.
```python
from kmk.macros.simple import send_string

WOW = send_string("Wow, KMK is awesome!")

keymap = [...WOW,...]
```
# Unicode
Before using unicode mode, you will need to set your platform. This can be done either of these ways.
You can use both in cases where you want to use one operating system, but occasionally use another.
This allows you to change modes on the fly without having to change your keymap.

	unicode_mode = UnicodeMode.LINUX
	Or
	keymap = [...KC.UC_MODE_LINUX,...]


### Unicode Modes:
On Linux IBUS is required, and on Windows, requires [WinCompose](https://github.com/samhocevar/wincompose)
- Linux : UnicodeMode.LINUX or UnicodeMode.IBUS
- Mac:    UnicodeMode.MACOS or UnicodeMode.OSX or UnicodeMode.RALT
- Windows: UnicodeMode.WINC

A note for IBUS users on Linux. This mode is not enabled by default, and will need to be turned on for this to work.
This works on X11, though if you are on Wayland, or in some GTK apps, it MAY work, but is not supported.

	export IBUS_ENABLE_CTRL_SHIFT_U=1

### Unicode Examples

To send a simple unicode symbol
```python
FLIP = unicode_string_sequence('(ノಠ痊ಠ)ノ彡┻━┻')
keymap = [...FLIP,...]
```

And for many single character unicode:

```python
from kmk.types import AttrDic

emoticons = AttrDict({
	'BEER': r'🍺',
	'HAND_WAVE': r'👋',
})

for k, v in emoticons.items():
emoticons[k] = unicode_string_sequence(v)

keymap = [...emoticons.BEER, emoticons.HAND_WAVE...]
```

If you need to send a unicode hex string, use unicode_codepoint_sequence()

```python
from kmk.macros.unicode import unicode_codepoint_sequence

TABLE_FLIP = unicode_codepoint_sequence([
	"28", "30ce", "ca0", "75ca","ca0", "29",
	"30ce", "5f61", "253b", "2501", "253b",
])

keymap = [...TABLE_FLIP,...]
```
