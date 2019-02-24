## Supported Devices

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857) | Atmel SAMD51 (Cortex M4F) | CircuitPython | An economical solution for basic USB keyboards |
| [Adafruit ItsyBitsy M4 Express](https://www.adafruit.com/product/3800) | Atmel SAMD51 (Cortex M4F) | CircuitPython | A smaller solution for basic USB keyboards |


## Support Planned/WIP
| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [Seeed nRF52840 Micro Dev Kit](https://www.seeedstudio.com/nRF52840-Micro-Development-Kit-p-3079.html) | nRF52840 | [CircuitPython](https://github.com/KMKfw/circuitpython/tree/topic-nrf52840-mdk) | This is basically as bleeding edge as it gets. Will support BLE HID to PC as well as BLE split boards |
| [Planck rev6 Keyboard](https://olkb.com/planck) | STM32 of some sort | MicroPython | Requires porting MicroPython to STM32F3, this work has begun but I'm pretty terrible at it. |
| [Proton C Controller?](https://www.reddit.com/r/MechanicalKeyboards/comments/87cw36/render_of_the_qmk_proton_c_qmkpowered_pro_micro/) | ??? | ??? | Does not exist yet, the controller from a Planck rev6 in a Pro Micro pin-compat controller chip |


## Unsupported Devices

Here's a list of problematic, but possibly usable microcontrollers:

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ------------------ |
| [Adafruit Feather Huzzah](https://www.adafruit.com/product/2821) | ESP8266 | CircuitPython | Suuuuuper limited on GPIO lanes, Lack USB HID (HW) |
| [Adafruit HUZZAH32](https://www.adafruit.com/product/3405) | ESP32 | MicroPython | This may work as a BLE HID device, or with a GPIO-based USB breakout. Lacks USB HID (HW) |
| [Adafruit Feather nRF52 BLE Controller](https://www.adafruit.com/product/3406) | nRF52832 | CircuitPython | Lacks USB HID (HW), but could be fixed with GPIO USB breakout. BLE HID should be possible, but it's considered somewhat unstable. This chip is considered "mostly unsupported" in CircuitPython at the time of writing. |

## Porting new devices
Pull requests are welcome and encouraged to add support for new
keyboards/microcontrollers. The base requirements for device support
- CircuitPython or MicroPython
- 256KB of flash storage
- HID over USB or Bluetooth.

## Secondary Support

In the future, secondary support for lesser controllers is planned. One of
these cases is the pro micro being used for a slave half of a split keyboard
while all actual work is being done by a supported board. This could also be
used to convert boards that use USB or i2c that run lesser chips to a KMK
board, with a supported board acting as a translation layer. Support for
a converter is planned with the inspiration coming from the [Hasu USB to
USB Controller Converter](https://www.1upkeyboards.com/shop/controllers/usb-to-usb-converter/) and would allow for conversion to KMK as
opposed to TMK or QMK with that board.