# Officially supported microcontrollers

While most CircuitPython devices are great for hand wired keyboards, most
keyboards are designed to accept a Pro Micro. The boards listed below either
are, or can be adapted to that pinout to use common keyboards already on the market.

## nice!nano

Features include

- Pro Micro pinout
- Both USB HID and Bluetooth support
- Can do Bluetooth split keyboards with no wires at all
- Has battery support including charging

Downsides

- $25 USD per microcontroller at most retailers

### Pre-compiling KMK for nice!nano

nice!nano has limited flash memory which does not fit CircuitPython, adafruit-ble, and KMK by default. You will need to use pre-compiled KMK to get it to fit. Grab [compatible mpy-cross](https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/) and run `make compile` to generate `.mpy` version of KMK files before copying them over.

Common Retailers

- [Boardsource](https://boardsource.xyz/store/5f4a1733bbaa5c635b83ed67)
- [Nice Keyboards](https://nicekeyboards.com/nice-nano/)

## ItsyBitsy M4 Express

Features include

- Affordable at $15 USD
- Can run most features of KMK including RGB

Downsides

- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)

Common Retailers

- [Adafruit](https://www.adafruit.com/product/3800)

## Raspberry Pi Pico

Features include

- Very affordable
- Very powerful for the price

Downsides

- Different form factor than a Pro Micro

Common Retailers

- [Adafruit](https://www.adafruit.com/pico?src=raspberrypi)
- [SparkFun](https://www.sparkfun.com/products/17829?src=raspberrypi)

## Adafruit ItsyBitsy nRF52840 Express

Features include

- Both USB HID and Bluetooth support
- More affordable than the nice!nano at only $18

Downsides

- Needs adapted to work with Pro Micro pinout keyboards. Adapter can be found
[HERE](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)
- No battery support without addon board found
[HERE](https://www.adafruit.com/product/2124)

Common Retailers

- [Adafruit](https://www.adafruit.com/product/4481)

## SparkFun Pro Micro (RP2040)

Features include

- RP2040-based, like the Raspberry Pi Pico
- Same form factor as the popular ATmega32U4-based Pro Micro and its siblings such as the Elite-C and Nullbits BIT-C
- Very affordable at ~$11

Downsides

- Popular ATmega32U4-based boards have I2C at pin positions 2 and 3. While the RP2040 supports using any pins between GPIO0 and GPIO29 as I2C, they need pull-up resistors. The only pins this board has resistors for are not easily accessible (see the positions of SDA and SCL [here](https://cdn.sparkfun.com/assets/e/2/7/6/b/ProMicroRP2040_Graphical_Datasheet.pdf)). This can be worked around by using pull-up resistors on pins GPIO2 and GPIO3, then [using the RP2040's PIO implementation](https://github.com/KMKfw/kmk_firmware/blob/master/docs/split_keyboards.md#rp2040-pio-implementation). This is only a consideration if the board is being used as a drop-in replacement for a ATmega32U4-based Pro Micro or equivalent *and* use of I2C is necessary.

Common Retailers

- [SparkFun](https://www.sparkfun.com/products/18288)

<details>
  <summary>Pro Micro Pin Conversion</summary>

| Pro Micro (ATmega32U4) | Pro Micro (RP2040) |
| ---------------------- | ------------------ |
| D3                     | GP0                |
| D2                     | GP1                |
| D1 (SDA)               | GP2                |
| D0 (SCL)               | GP3                |
| D4                     | GP4                |
| C6                     | GP5                |
| D7                     | GP6                |
| E6                     | GP7                |
| B4                     | GP8                |
| B5                     | GP9                |
| F4                     | GP29/A3            |
| F5                     | GP28/A2            |
| F6                     | GP27/A1            |
| F7                     | GP26/A0            |
| B1                     | GP22               |
| B3                     | GP20               |
| B2                     | GP23               |
| B6                     | GP21               |

</details>

## Adafruit KB2040

Features include

- RP2040-based, like the Raspberry Pi Pico
- Same form factor as the popular ATmega32U4-based Pro Micro and its siblings such as the Elite-C and Nullbits BIT-C
- Very affordable at ~$9
- I2C pin positions match the ATmega32U4-based Pro Micro

Common Retailers

- [Adafruit](https://www.adafruit.com/product/5302)
- [Pimoroni](https://shop.pimoroni.com/products/adafruit-kb2040-rp2040-kee-boar-driver)

<details>
  <summary>Pro Micro Pin Conversion</summary>

| Pro Micro (ATmega32U4) | KB2040 |
| ---------------------- | ------ |
| D3                     | D0     |
| D2                     | D1     |
| D1 (SDA)               | D2     |
| D0 (SCL)               | D3     |
| D4                     | D4     |
| C6                     | D5     |
| D7                     | D6     |
| E6                     | D7     |
| B4                     | D8     |
| B5                     | D9     |
| F4                     | A3     |
| F5                     | A2     |
| F6                     | A1     |
| F7                     | A0     |
| B1                     | SCK    |
| B3                     | MISO   |
| B2                     | MOSI   |
| B6                     | D10    |

</details>

## Other microcontrollers

What you'll need to have at minimum

- CircuitPython
- 256KB of flash storage
- HID over USB and/or Bluetooth.
