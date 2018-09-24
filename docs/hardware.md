## Supported Devices

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [pyboard v1.1](https://www.adafruit.com/product/2390) | STM32F405RG (Cortex M4F) | MicroPython | A very basic keyboard has been written for this, see `boards/klardotsh/threethree_matrix_pyboard.py` |

### Support Planned/WIP
| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [Seeed nRF52840 Micro Dev Kit](https://www.seeedstudio.com/nRF52840-Micro-Development-Kit-p-3079.html) | nRF52840 | [MicroPython](https://github.com/klardotsh/micropython/commit/4eac11a6d1ba2d269b4cdc663d4b5b788b288804) | This is basically as bleeding edge as it gets. Linked is my very unstable and somewhat broken uPy port to this device, WIP. Supports BLE HID and, allegedly, USB HID if I can figure it out. Another option is CircuitPython, since AdaFruit is working on a Feather Express with the same chipset, and commits have been made there to support USB HID. |
| [Planck rev6 Keyboard](https://olkb.com/planck) | STM32 of some sort | Probably MicroPython? | I have one on the way! We'll see what happens. |
| [Proton C Controller?](https://www.reddit.com/r/MechanicalKeyboards/comments/87cw36/render_of_the_qmk_proton_c_qmkpowered_pro_micro/) | ??? | ??? | Does not exist yet, the controller from a Planck rev6 in a Pro Micro pin-compat controller chip |


## Unsupported Devices

If you don't see it in "Supported Devices", it won't work out of the box, it's
basically that simple. Pull requests are welcome and encouraged to add support
for new keyboards. The base requirements for device support are a port of
CircuitPython or MicroPython, at least 256KB of flash storage, and USB and/or 
Bluetooth LE interfaces.

Here's a list of boards that seem like they should otherwise be supported, but
are currently not, due to some deficiency uncovered in development/testing:

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ------------------ |
| [Adafruit Feather Huzzah](https://www.adafruit.com/product/2821) | ESP8266 | CircuitPython | Suuuuuper limited on GPIO lanes, Lack of USB HID (HW) |
| [Adafruit HUZZAH32](https://www.adafruit.com/product/3405) | ESP32 | MicroPython | In theory this may work as a BLE HID device, or with a GPIO-based USB breakout. Right now, we haven't written the code for this device. Built-in USB port can't run in HID at all. |
| [Adafruit Feather nRF52 BLE Controller](https://www.adafruit.com/product/3406) | nRF52832 | CircuitPython | Lack of USB HID (HW), but could be fixed with GPIO USB breakout. BLE HID could be possible, but it's considered somewhat unstable. This chip is considered "mostly unsupported" in CircuitPython according to Adafruit Discord, so I've mostly abandoned it for now. |
| [Teensy 3.2 Controller](https://www.adafruit.com/product/2756) | | MicroPython | Lack of USB HID (SW - MP) |


## The Great Hackaround

While it is required that at least the device talking over USB/BLE HID (the
"primary brain") be from the Supported Devices list and running the primary
component of KMK, it will soon be possible to build split keyboards with other,
otherwise unsupported devices (currently this means a Pro Micro), either to
reduce costs or to convert existing QMK boards to KMK. You'll need to flash
"dummy" firmware to each Pro Micro which simply scans a matrix and passes the
values over I2C to the "brain" device, which does the heavy lifting from there
(including actually sending HID events).

The obvious downsides of this method are increased number of moving parts,
increased number of things to flash (though the Pro Micros only need flashed
when matricies change, which should almost never happen once a board is built),
and all downsides that go with those points (increased power usage, etc.) The
upside is that it can be a _ton_ cheaper to build a split keyboard this way -
cheapo Pro Micro clones can be had for as little as $4 CAD at time of writing,
whereas a HUZZAH32, for example, is closer to $26 CAD, and to build the
"traditional" way, you'd need N of them (where N is the number of split sections
of your keyboard).

It is also possible to convert many QMK boards through this fashion - while
untested for now, just about anything with a TRRS jack should work (Ergodoxen,
just about anything from keeb.io, etc.) 

This hackaround is almost certainly pointless for non-split boards.

