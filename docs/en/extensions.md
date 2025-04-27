# Extensions

Extensions add features that change the experience, but not the core features of
the keyboard. They are meant to be easy to add, and create your own. These live in
a sandbox to help prevent any bad code from crashing your keyboard.

## Core Extensions

These extensions are provided in all builds and can be enabled. Currently offered
extensions are

- [International](international.md): Adds international keycodes
- [LED](led.md): Adds backlight support. This is for monocolor backlight, not RGB
- [LockStatus](lock_status.md): Exposes host-side locks like caps or num lock.
- [MediaKeys](media_keys.md): Adds support for media keys such as volume
- [OLED Displays](OLED_display.md): Support for common OLED displays.
- [RGB](rgb.md): RGB lighting for underglow. Will work on most matrix RGB as will
  be treated the same as underglow.
- [SpaceMouse Status](spacemouse_status.md): Exposes host-side LED status of the SpaceMouse HID.
- [Status LED](extension_statusled.md): Indicates which layer you are on with an array of single leds.
- [Stringy Keymaps](extension_stringy_keymaps): Enables referring to keys by `'NAME'` rather than `KC.NAME`
