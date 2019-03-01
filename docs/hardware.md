## Supported Devices

| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [Adafruit Feather M4 Express](https://www.adafruit.com/product/3857) | Atmel SAMD51 (Cortex M4F) | CircuitPython | An economical solution for basic USB keyboards |
| [Adafruit ItsyBitsy M4 Express](https://www.adafruit.com/product/3800) | Atmel SAMD51 (Cortex M4F) | CircuitPython | A smaller solution for basic USB keyboards |
| [Adafruit Feather NRF52840 Express](https://www.adafruit.com/product/4062) | Cortex M4F/nrf52840 | CircuitPython | Supports USB HID and soon BLE (Bluetooth) |
| [Seeed nRF52840 Micro Dev Kit](https://www.seeedstudio.com/nRF52840-Micro-Development-Kit-p-3079.html) | M4F/nrf52840 | CircuitPython | Supports USB HID and soon BLE (Bluetooth) |


## Support Planned/WIP
| Board | Chipset | Python Platform | Notes |
| ----- | ------- | --------------- | ----- |
| [Planck rev6 Keyboard](https://olkb.com/planck) | STM32F303 | CircuitPython | Requires porting CircuitPython to STM32F3. |
| [Proton C Controller?](https://olkb.com/parts/qmk-proton-c) | STM32F303CCT6 | CircuitPython | Requires porting CircuitPython to STM32F3. |



## Porting new devices
Pull requests are welcome and encouraged to add support for new
keyboards/microcontrollers. The base requirements for device support
- CircuitPython
- 256KB of flash storage
- HID over USB and/or Bluetooth.

## Secondary Support

In the future, secondary support for lesser controllers is planned. One of
these cases is the pro micro being used for a slave half of a split keyboard
while all actual work is being done by a supported board. This could also be
used to convert boards that use USB or i2c that run lesser chips to a KMK
board, with a supported board acting as a translation layer. Support for
a converter is planned with the inspiration coming from the [Hasu USB to
USB Controller Converter](https://www.1upkeyboards.com/shop/controllers/usb-to-usb-converter/)
and would allow for conversion to KMK as opposed to TMK or QMK with that board.