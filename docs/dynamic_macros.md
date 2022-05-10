# Dynamic Macros
Dynamic macros allow you to record a macro just by typing it without modifying your firmware.  Any macro recorded this way is temporary and  will remain available until your keyboard reboots.

### How to use
#### Recording
1. Press record
2. Type your macro
3. Press stop

#### Playing
1. Press play to use your recorded macro

## Enable dynamic macros
```python
from kmk.modules.dynamic_macros import DynamicMacros

keyboard.modules.append(DynamicMacros())
```

## Keycodes
|Key                         |Description                            |
|----------------------------|---------------------------------------|
|`KC.RECORD_MACRO()`         |Start recording into the current slot  |
|`KC.PLAY_MACRO()`           |Play the macro in the current slot     |
|`KC.STOP_MACRO()`           |Stop recording, playing, or configuring|
|`KC.SET_MACRO(x)`           |Change to the macro in slot `x`        |
|`KC.SET_MACRO_REPETITIONS()`|Change to repepition config mode       |
|`KC.SET_MACRO_INTERVAL()`   |Change to interval config mode         |

## Config
```python
dynamicMacros = DynamicMacros(
    slots=1, # The number of macro slots to use
    timeout=60000,  # Maximum time to spend in record or config mode before stopping automatically, miliseconds
    key_interval=0,  # Miliseconds between key events while playing
    use_recorded_speed=False  # Whether to play the macro at the speed it was typed
)
```

## Macro slots
You can configure multiple slots that each store a different macro.  You can change to a specific slot with `KC.SET_MACRO(x)`, where `x` is the macro slot number (starting from `0`).  Every keycode can take an optional number to change to a specific macro slot before performing the action.  For example `KC.PLAY_MACRO(2)` will play the macro in slot `2`.  If a slot is not specified, the current slot will be used.

## Repeating macros
Macros can be set to repeat automatically.  The number of repetitions and the interval between repetitions can be set using `KC.SET_MACRO_REPETITIONS()` and `KC.SET_MACRO_INTERVAL()`.  Using one of these keys will put the keyboard in macro config mode.  In this mode, keypresses will not be sent to the OS and you can use your number keys to type the number of repetitions or the interval time in seconds.  This mode ends when you press `KC.ENTER`, `KC.STOP_MACRO()`, or automatically when the timeout is reached.  Repeat settings are stored in the current slot.