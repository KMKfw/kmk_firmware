# Leader Key
The leader key acts as a prefix to a key sequence. These can be used to trigger macros quickly
without dedicated keys set to each function. For those of you who dislike key combos, such as
Ctrl+Shift+Esc, then this feature is for you. This is very much inspired from vim.

## Keycode
|Key                    |Description                                                          |
|-----------------------|---------------------------------------------------------------------|
|`KC.LEAD`              |The [Leader key]                                                     |

# Enabling the extention
```python
from kmk.extensions.leader import Leader
from kmk.handlers.sequences import send_string

leader_ext = Leader(}
)
 
keyboard.extensions.append(leader_ext)

```

Leader key sequences can be as long or short as you like. The action be a keycode, or
can be things like unicode macros, or generic macros. The example below shows how you would
trigger task manager in Windows with a leader sequence.

1. Assign a key to KC.LEAD
2. Above your keymap, include a LEADER_DICTIONARY.

```python
from kmk.macros.simple import simple_key_sequence

# ...

leader_ext = Leader(
    sequences={
    'task': : simple_key_sequence([Modifiers.KC_LCTRL(Modifiers.KC_LSHIFT(Common.KC_ESC))])
    }
)

keymap = [...KC.LEAD,...]

# ...
```


# Modes
1. LeaderMode.TIMEOUT (the default)
2. LeaderMode.ENTER

### Timeout Mode
Will expire after a timer and trigger the sequence that matches if any. The default timeout is 1000ms

### Enter Mode
Has no timeout. To end sequence press the enter key, or cancel and do nothing, press escape.

## Changing defaults
To change the mode or timeout, add them here
```python
from kmk.extensions.leader import Leader, LeaderMode
leader_ext = Leader(
    mode=LeaderMode.ENTER,
    timeout=1000
    sequences={
    'hello': send_string('hello world from kmk macros'),
    }
)
```
