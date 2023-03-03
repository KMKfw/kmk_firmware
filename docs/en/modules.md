# Modules
Modules, unlike extensions, change how your keyboard works. These are meant to have
the ability to alter the core code in any way. Unlike extensions, these are not in a
sandbox, and can make massive changes to normal operation.

## Core Modules
These modules are provided in all builds and can be enabled. Currently offered
modules are

- [Combos](combos.md): Adds chords and sequences
- [Layers](layers.md): Adds layer support (Fn key) to allow many more keys to be
put on your keyboard.
- [HoldTap](holdtap.md): Adds support for augmented modifier keys to act as one key
when tapped, and modifier when held.
- [Mouse keys](mouse_keys.md): Adds mouse keycodes.
- [OneShot](oneshot.md): Adds support for oneshot/sticky keys.
- [Power](power.md): Power saving features. This is mostly useful when on battery power.
- [Split](split_keyboards.md): Keyboards split in two. Seems ergonomic!
- [SerialACE](serialace.md): [DANGER - _see module README_] Arbitrary Code Execution over the data serial.
- [TapDance](tapdance.md): Different key actions depending on how often it is pressed.
- [Dynamic Sequences](dynamic_sequences.md): Records a sequence of keypresses and plays it back.

### Require Libraries
These modules can be used without specific hardware, but require additional libraries such as the `Adafruit CircuitPython Bundle`.

 - [MIDI](midi.md): Adds sending MIDI data in the form of keymap entries.


### Peripherals
These modules are for specific hardware and may require additional libraries to function.
- [ADNS9800](adns9800.md): Controlling ADNS9800 optical sensor.
- [Encoder](encoder.md): Handling rotary encoders.
- [Pimoroni trackball](pimoroni_trackball.md): Handling a small I2C trackball made by Pimoroni.
- [AS5013 aka EasyPoint](easypoint.md): Handling a small I2C magnetic position sensor made by AMS.
