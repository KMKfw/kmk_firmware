# Lunakey Pico

![Lunakey Pico](https://s2.booth.pm/08af5e15-6203-47a9-9ff4-0e949a678a9b/i/3324672/0b811a3b-27e8-412a-8aa5-57e2880afddb_base_resized.jpg)

Lunakey Pico is a 40% keyboard which has 44 keys and is split to left and right. Each side has 3 rows x 6 columns and 4 keys that are pressed by a thumb. Also, it has an ability to light up by Underglow LEDs on the bottom and an ability to play a sound by a speaker module. Of course, the column-staggered key layout is the result of deep thinking to fit each finger and each key naturally.

* 40% keyboard (3 rows and 6 columns for each side).
* Column-staggered key layout to fit each length of fingers.
* 4 keys for thumb fitted to range of movement of the finger naturally.
* Supported both Cherry MX compatible key switches and Kailh Choc low profile key switches.
* Can exchange key switches without soldering by adopting the key sockets.
* Underglow LEDs lighting effect.
* Provides a sound feedback by a piezoelectric speaker.

The special feature of this Lunakey Pico is that [Raspberry Pi Pico](https://www.raspberrypi.org/products/raspberry-pi-pico/) has been adopted. Users can use some firmwares including [KMK Firmware](https://github.com/KMKfw/kmk_firmware).

Hardware Availability: [PCB & Case Source](https://github.com/yoichiro/lunakey#lunakey-pico)

Retailers: [Lunakey Pico - Yoichiro's Garage - BOOTH](https://yoichiro.booth.pm/items/3324672)

## Dependencies

* [neopixel.py](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel) - It is necessary to turn on the Underglow LEDs.
* [pwmio](https://circuitpython.readthedocs.io/en/latest/shared-bindings/pwmio/index.html) - It is necessary to support a sound feedback with a piezoelectric speaker.
