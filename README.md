# KMK: Clackety Keyboards Powered by Python
![GitHub](https://img.shields.io/github/license/KMKfw/kmk_firmware)
![GitHub contributors](https://img.shields.io/github/contributors/KMKfw/kmk_firmware)
![Lines of code](https://img.shields.io/tokei/lines/github/KMKfw/kmk_firmware)
![GitHub issues](https://img.shields.io/github/issues-raw/KMKfw/kmk_firmware)
![GitHub closed issues](https://img.shields.io/github/issues-closed/KMKfw/kmk_firmware)

KMK is a feature-rich and beginner-friendly firmware for computer keyboards
written and configured in
[CircuitPython](https://github.com/adafruit/circuitpython).

## Support

For asynchronous support and chatter about KMK, [join our Zulip
community](https://kmkfw.zulipchat.com)!

If you ask for help in chat or open a bug report, if possible
make sure your copy of KMK is up-to-date.
In particular, swing by the Zulip chat *before* opening a GitHub Issue about
configuration, documentation, etc. concerns.

> The former Matrix and Discord rooms once linked to in this README are no
> longer officially supported, please do not use them!

## Features

- Fully configured through a single, easy to understand Python file that lives
  on a "flash-drive"-esque space on your microcontroller - edit on the go
  without DFU or other dev tooling available!
- Single-piece or [two-piece split
  keyboards](/docs/en/split_keyboards.md)
  are supported
- [Chainable
  keys](/docs/en/keys.md) such as
  `KC.LWIN(KC.L)` to lock the screen on a Windows PC
- [Built-in Unicode macros, including
  emojis](/docs/en/sequences.md)
- [RGB underglow](/docs/en/rgb.md)
  and [LED
  backlights](/docs/en/led.md)
- One key can turn into many more based on [how many times you tap
  it](/docs/en/tapdance.md)
- Bluetooth HID and split keyboards. No more wires.

## Getting Started
KMK requires [CircuitPython](https://circuitpython.org/) version 7.0 or higher.
Our getting started guide can be found
[here](/docs/en/Getting_Started.md).

## Contributing

Please have a look at the [contributing document](/docs/en/contributing.md), 
where you can find details about the workflow and code style. If you have 
specific questions feel free to ask in the [KMK development stream](https://kmkfw.zulipchat.com/#narrow/stream/384078-KMK-development) 
on Zulip.

## License, Copyright, and Legal

All software in this repository is licensed under the [GNU Public License,
version 3](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)).
All documentation and hardware designs are licensed under the [Creative Commons
Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
license.

**Due to ethical and legal concerns, any works derived from GitHub Copilot or
similar artificial intelligence tooling are unacceptable for inclusion in any
first-party KMK repository or other code collection. We further recommend not
using GitHub Copilot while developing anything KMK-related, regardless of
intent to submit upstream.**
