# Dynamic Sequences
Dynamic sequences allow you to record a sequence just by typing it without modifying your keymap.  Any sequence recorded this way is temporary and  will remain available until your keyboard reboots.

### How to use
#### Recording
1. Press record
2. Type your sequence
3. Press stop

#### Playing
1. Press play to use your recorded sequence

## Enable dynamic sequences
```python
from kmk.modules.dynamic_sequences import DynamicSequences

keyboard.modules.append(DynamicSequences())
```

## Keycodes
|Key                            |Description                            |
|-------------------------------|---------------------------------------|
|`KC.RECORD_SEQUENCE()`         |Start recording into the current slot  |
|`KC.PLAY_SEQUENCE()`           |Play the sequence in the current slot  |
|`KC.STOP_SEQUENCE()`           |Stop recording, playing, or configuring|
|`KC.SET_SEQUENCE(x)`           |Change to the sequence in slot `x`     |
|`KC.SET_SEQUENCE_REPETITIONS()`|Change to repetition config mode       |
|`KC.SET_SEQUENCE_INTERVAL()`   |Change to interval config mode         |

## Config
```python
dynamicSequences = DynamicSequences(
    slots=1, # The number of sequence slots to use
    timeout=60000,  # Maximum time to spend in record or config mode before stopping automatically, milliseconds
    key_interval=0,  # Milliseconds between key events while playing
    use_recorded_speed=False  # Whether to play the sequence at the speed it was typed
)
```

## Sequence slots
You can configure multiple slots that each store a different sequence.  You can change to a specific slot with `KC.SET_SEQUENCE(x)`, where `x` is the sequence slot number (starting from `0`).  Every keycode can take an optional number to change to a specific sequence slot before performing the action.  For example `KC.PLAY_SEQUENCE(2)` will play the sequence in slot `2`.  If a slot is not specified, the current slot will be used.

## Repeating sequences
Sequences can be set to repeat automatically.  The number of repetitions and the interval between repetitions can be set using `KC.SET_SEQUENCE_REPETITIONS()` and `KC.SET_SEQUENCE_INTERVAL()`.  Using one of these keys will put the keyboard in sequence config mode.  In this mode, keypresses will not be sent to the OS and you can use your number keys to type the number of repetitions or the interval time in seconds.  This mode ends when you press `KC.ENTER`, `KC.STOP_SEQUENCE()`, or automatically when the timeout is reached.  Repeat settings are stored in the current slot.