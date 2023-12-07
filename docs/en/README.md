# Documentation index

Before you look further, you probably want to start with our [getting started guide](basics/Getting_Started.md).

## [Basics](basics)

- [Getting Started](basics/Getting_Started.md)
- [Bluetooth HID](basics/ble_hid.md): Connect keyboard to PC or mobile device using BLE
- [Configuring KMK](basics/config_and_keymap.md)
- [Porting to KMK](basics/porting_to_kmk.md): Creating a `kb.py` file for a board
- [Debugging](basics/debugging.md)
- [Keycodes](basics/keycodes.md): List of all available keycodes
- [Officially supported microcontrollers](basics/Officially_Supported_Microcontrollers.md)
- [Support](basics/support.md)
- [Contributing](basics/contributing.md)

## [Advanced](advanced)

- [Flashing instructions](advanced/flashing.md)
- [Handwiring](advanced/handwiring.md): Resources helpful when handwiring a keyboard circuit
- [Keys](advanced/keys.md): Technical explanation of key handling
- [Scanners](advanced/scanners.md): Setting up non-default key reading

## [Modules](modules/index.md)

- [Combos](modules/combos.md): Adds chords and sequences
- [Layers](modules/layers.md): Adds layer support (Fn key) to allow many more keys to be put on your keyboard
- [HoldTap](modules/holdtap.md): Adds support for augmented modifier keys to act as one key when tapped, and modifier when held.
- [Mouse keys](modules/mouse_keys.md): Adds mouse keycodes
- [OneShot](modules/oneshot.md): Adds support for oneshot/sticky keys.
- [Power](modules/power.md): Power saving features. This is mostly useful when on battery power.
- [SerialACE](modules/serialace.md): [DANGER - _see module README_] Arbitrary Code Execution over the data serial.
- [Split](modules/split_keyboards.md): Keyboards split in two. Seems ergonomic!
- [TapDance](modules/tapdance.md): Different key actions depending on how often it is pressed.

### [Peripherals](peripherals)

- [ADNS9800](peripherals/adns9800.md): Controlling ADNS9800 optical sensor
- [Encoder](peripherals/encoder.md): Handling rotary encoders
- [Pimoroni trackball](peripherals/pimoroni_trackball.md): Handling a small I2C trackball made by Pimoroni

## [Extensions](extensions/index.md)

- [International](extensions/international.md): Adds international keycodes
- [LED](extensions/led.md): Adds backlight support. This is for monocolor backlight, not RGB
- [LockStatus](extensions/lock_status.md): Exposes host-side locks like caps or num lock.
- [MediaKeys](extensions/media_keys.md): Adds support for media keys such as volume
- [RGB](extensions/rgb.md): RGB lighting for underglow. Will work on most matrix RGB as will be treated the same as underglow.
- [Status LED](extensions/status_led.md): Indicates which layer you are on with an array of single leds.

## Language versions

- [Japanese getting started](../ja/Getting_Started.md)
- [Brazilian Portuguese](../ptBR)
