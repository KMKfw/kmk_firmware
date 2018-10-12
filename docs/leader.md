# Leader Key
The leader key acts as a prefix to a key sequence. These can be used to trigger macros quickly
without dedicated keys set to each function. For those of you who dislike key combos, such as
Ctrl+Shift+Esc, then this feature is for you. This is very much inspired from vim.

Leader key sequences can be as long or short as you like. The action must be a macro, so it
can be things like unicode macros, or generic macros. The example below shows how you would
trigger task manager in Windows with a leader sequence. By default Leader Mode is ENTER, which
means that after your sequence you will hit ENTER to trigger the sequence completion, or ESC to
cancel the sequence.

1. Assign a key to KC.LEAD
2. Above your keymap, include a LEADER_DICTIONARY.

```python
from kmk.macros.simple import simple_key_sequence

LEADER_DICTIONARY = {
	(KC.T, KC.A, KC.S, KC.K): simple_key_sequence(Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_ESC)))
}

keymap = [...KC.LEAD,...]
```
# Modes
Modes avaliable (WARNING: LeaderMode.ENTER is currently the only one avaliable.)
1. LeaderMode.DEFAULT
2. LeaderMode.ENTER

### DEFAULT #WARNING# NOT AVALIBLE YET
Will expire after a timer and trigger the sequence that matches if any.
This can be enabled with
```python
from kmk.consts.LederMode
leader_mode = LeaderMode.DEFAULT
```
The timeout can be set like this
```python
leader_timeout = 2000
```
### ENTER
Has no timeout. To end sequence press the enter key, or cancel and do nothing, press escape.
This can be enabled with

	from kmk.consts.LederMode
	leader_mode = LeaderMode.ENTER

