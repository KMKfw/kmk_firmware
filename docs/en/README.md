# Documentation index

> Before you look further, you probably want to start with our [getting started guide](/docs/en/Getting_Started.md)

## Basics

- [Getting Started](Getting_Started.md)
- [Bluetooth HID](ble_hid.md): Connect keyboard to PC or mobile device using BLE
- [Configuring KMK](config_and_keymap.md)
- [Porting to KMK](porting_to_kmk.md): Creating a `kb.py` file for a board
- [Debugging](debugging.md)
- [Keycodes](keycodes.md): List of all available keycodes
- [Officially supported microcontrollers](Officially_Supported_Microcontrollers.md)
- [Support](support.md)
- [Contributing](contributing.md)

## Advanced

- [Flashing instructions](flashing.md)
- [Handwiring](handwiring.md): Resources helpful when handwiring a keyboard circuit
- [Keys](keys.md): Technical explanation of key handling
- [Scanners](scanners.md): Setting up non-default key reading

## [Modules](modules.md)

- [Combos](combos.md): Adds chords and sequences
- [Layers](layers.md): Adds layer support (Fn key) to allow many more keys to be put on your keyboard
- [HoldTap](holdtap.md): Adds support for augmented modifier keys to act as one key when tapped, and modifier when held.
- [Mouse keys](mouse_keys.md): Adds mouse keycodes
- [OneShot](oneshot.md): Adds support for oneshot/sticky keys.
- [Power](power.md): Power saving features. This is mostly useful when on battery power.
- [SerialACE](serialace.md): [DANGER - _see module README_] Arbitrary Code Execution over the data serial.
- [Split](split_keyboards.md): Keyboards split in two. Seems ergonomic!
- [TapDance](tapdance.md): Different key actions depending on how often it is pressed.

### Peripherals

- [ADNS9800](adns9800.md): Controlling ADNS9800 optical sensor
- [Encoder](encoder.md): Handling rotary encoders
- [Pimoroni trackball](pimoroni_trackball.md): Handling a small I2C trackball made by Pimoroni

## [Extensions](extensions.md)

- [International](international.md): Adds international keycodes
- [LED](led.md): Adds backlight support. This is for monocolor backlight, not RGB
- [LockStatus](lock_status.md): Exposes host-side locks like caps or num lock.
- [MediaKeys](media_keys.md): Adds support for media keys such as volume
- [RGB](rgb.md): RGB lighting for underglow. Will work on most matrix RGB as will be treated the same as underglow.
- [Status LED](extension_statusled.md): Indicates which layer you are on with an array of single leds.

## Language versions

- [Japanese getting started](https://github.com/KMKfw/kmk_firmware/tree/master/docs/ja/Getting_Started.md)
- [Brazilian Portuguese](https://github.com/KMKfw/kmk_firmware/tree/master/docs/ptBR)
