# MIDI
The MIDI module adds keymap entries for sending MIDI data streams. It will require adding the `adafruit_midi` library from the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries) to your device's folder.  
Add it to your keyboard's modules list with:

```python
from kmk.modules.midi import MidiKeys
keyboard.modules.append(MidiKeys())
```
## Keycodes

|Key                            |Description                                               |
|-------------------------------|----------------------------------------------------------|
|`KC.MIDI_CC(ctrl, val)`        |Sends a ControlChange message                             |
|`KC.MIDI_NOTE(note, velo)`     |Sends a Note message                                      |
|`KC.MIDI_PB(val)`              |Sends a Pitch Wheel message                               |
|`KC.MIDI_PC(program)`          |Sends a Program Change message                            |
|`KC.MIDI_START()`              |Sends a Start message                                     |
|`KC.MIDI_STOP()`               |Sends a Stop message                                      |