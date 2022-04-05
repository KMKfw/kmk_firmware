# Sofle V2

![Sofle V2](https://github.com/josefadamcik/SofleKeyboard)

"Sofle is 6×4+5 keys column-staggered split keyboard with encoder support. Based on Lily58, Corne and Helix keyboards."

Hardware Availability: [PCB & Case Source](https://github.com/josefadamcik/SofleKeyboard)  

`kb.py` is designed to work with the [SparkFun Pro Micro RP2040](https://www.sparkfun.com/products/18288).

Retailers
[beekeeb (Hong Kong)](https://shop.beekeeb.com/product/sofle-v2-soflekeyboard-v2-0-1-split-ergonomic-diy-mechanical-keyboard-pcb-kit/)
[Ergomech Store (Vietnam)](https://ergomech.store/shop/product/sofle-v2-2#attr=5,23)

Extentions enabled by default  
- [Layers](https://github.com/KMKfw/kmk_firmware/blob/master/docs/layers.md) "Layers module adds keys for accessing other layers."
- [Split](https://github.com/KMKfw/kmk_firmware/blob/master/docs/split_keyboards.md) Connects halves with or without wires (currently uses wires)
    - You must add the `adafruit_pioasm.mpy` to the `lib` folder on the RP2040 for this code to work. More about this is described [here](https://github.com/KMKfw/kmk_firmware/blob/master/docs/split_keyboards.md#rp2040-pio-implementation).
- [Encoder](https://github.com/KMKfw/kmk_firmware/blob/master/docs/encoder.md) "Add twist control to your keyboard!"

## Notes

- This keymap I used the [default used by QMK for Sofle](https://github.com/qmk/qmk_firmware/blob/master/keyboards/sofle/keymaps/default/keymap.c) (I only used QWERTY, RAISE and LOWER)
- As of 2022-04-05: Only one encoder will work at the moment. The side that is plugged in will work and the way I wrote it is designed to work with the left plugged in. If the right is plugged in the encoder will work but the encoder will work backwards.
- It is possible that the KMK code used for the Sofle V2 could be used on the Sofle V1 or the Sofle RGB or the Sofle Choc. These would each need to be tested to see if they work.
