# MIDI
The MIDI module adds keymap entries for sending MIDI data streams. It will require adding the `adafruit_midi` library from the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) to your device's folder.  
Add it to your keyboard's modules list with:

```python
from kmk.modules.midi import MidiKeys
keyboard.modules.append(MidiKeys())
```
## Keycodes

|Key         |Description                                                                  |
|-----------------|------------------------------------------------------------------------|
|`KC.MIDI_CC()`      |Sends a ControlChange message; accepts two integer arguments of `0`-`15`(controller number) then `0`-`127`(control value)                                           |
|`KC.MIDI_NOTE()`      |Sends a Note message with both 'On' and 'Off' segments; accepts two integer arguments of `0`-`127`(note number) and `0`-`127`(velocity)            |
|`KC.MIDI_PB()` |Sends a Pitch Wheel message; accepts a single integer argument of `0`-`16383`, centered on `8192`                                 |
|`KC.MIDI_PC()`  |Sends a Program Change message; accepts a single integer argument of `0`-`127`(program number)               |
|`KC.MIDI_START()`      |Sends a Start message; accepts no arguments          |
|`KC.MIDI_STOP()`      |Sends a Stop message; accepts no arguments                     |