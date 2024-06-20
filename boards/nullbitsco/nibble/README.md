Keyboard mapping for the [nullbits nibble](https://nullbits.co/nibble/).

Copy `kb.py` and `main.py` to your top level CircuitPython folder beside the kmk folder.
Edit the key mapping in `main.py` to match your keyboard layout.

The Keyboard constructor supports an optional `encoder` argument (see `kb.py`).
See the sample `main.py` for an example of how to configure the encoder.

The RGB extension in the example requires a copy of `neopixel.py` in your top level
CircuitPython folder: see https://github.com/KMKfw/kmk_firmware/blob/main/docs/en/rgb.md.
