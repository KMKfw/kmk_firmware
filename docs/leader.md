# Leader Key
The leader key acts as a prefix to a key sequence. These can be used to trigger macros quickly
without dedicated keys set to each function. For those of you who dislike key combos, such as
Ctrl+Shift+Esc, then this feature is for you. This is very much inspired from vim.

Leader key sequences can be as long or short as you like. The action must be a macro, so it
can be things like unicode macros, or generic macros. The example below shows how you would
trigger task manager in Windows with a leader sequence.

1. Assign a key to KC.LEAD
2. Above your keymap, include a LEADER_DICTIONARY.

```python
from kmk.macros.simple import simple_key_sequence

# ...

keyboard.leader_dictionary = {
    (KC.T, KC.A, KC.S, KC.K): simple_key_sequence([Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_ESC))])
}

keymap = [...KC.LEAD,...]

# ...
```

If defining tuples of keycodes is too obtuse for you, we have a convenience
function available for that, too!

```python
from kmk.keycodes import generate_leader_dictionary_seq as glds

# ...

keyboard.leader_dictionary = {
    glds('task'): simple_key_sequence([Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_ESC))])
}

# ...
```

# Modes
1. LeaderMode.TIMEOUT (the default)
2. LeaderMode.ENTER

### Timeout Mode
Will expire after a timer and trigger the sequence that matches if any.
This can be enabled with
```python
from kmk.consts import LeaderMode
keyboard.leader_mode = LeaderMode.TIMEOUT
```

The timeout can be set like this
```python
keyboard.leader_timeout = 2000  # in milliseconds-ish
```

The timeout defaults to `1000`, which is roughly a second.

### Enter Mode
Has no timeout. To end sequence press the enter key, or cancel and do nothing, press escape.
This can be enabled with

```python
from kmk.consts import LeaderMode
keyboard.leader_mode = LeaderMode.ENTER
```
