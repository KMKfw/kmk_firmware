# Piantor

The [Piantor by beekeeb](https://github.com/beekeeb/piantor), is a 36- or 42-key staggered column, diodeless keyboard. It is based on the [Cantor by Diego Palacios](https://github.com/diepala/cantor), but uses a Raspberry Pi Pico as the controller.

The default keymap replicates the Corne/crkbd default keymap by foostan and drashna.

Purchase: [BeeKeeb](https://shop.beekeeb.com/product/piantor-keyboard-kit/)

## Microcontroller and Split Support
This firmware assumes that VBUS will be used for split side detection as in the QMK implementation. This requires that the USB cable is plugged into the left side to ensure that the correct pin mapping is used. If using a rp2040 microcontroller without a VBus sense circuit (like the WeAct RP2040), resistors must be soldered to the bottom of the PCBs, and you will need to uncomment line 9 of kb.py to assign the VBus sense pin to GP24.

An alternative option is to detect the split sides using the drive names. See the [KMK documentation](http://kmkfw.io/docs/split_keyboards#drive-names) for setting this up. Once you have set drive names, you can comment out lines 12-14 and uncomment lines 17-18 in kb.py to enable this option.
