# Psion Keyboards

Keyboard from an old [Psion Series 5mx](https://en.wikipedia.org/wiki/Psion_Series_5) handheld computer, driven by a custom RP2040 adapter.

Currently supported layouts:

- Swedish
- UK

## Installation

### Step 1 - Install CircuitPython

1. Download [CircuitPython for the Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/)
1. Follow the [installation instructions](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)


### Step 2 - Install KMK

1. Get an up to date [copy of KMK](https://github.com/KMKfw/kmk_firmware/archive/refs/heads/main.zip)
1. Unzip it and copy the KMK folder and the boot.py to your[CIRCUITPY drive](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive)


### Step 3 - Install these files

Copy these files to your CIRCUITPY drive. If there is a `layout_xxx.py` file you won't need, you can skip it.

- `code.py`
- `layout_swe.py`
- `layout_xxx.py`

### Step 4 - Select your layout

On your CIRCUITPY drive, open the file `code.py` in a text editor. Close to the end of the file, you'll find a section that looks like this:

```python
# Choose your layout here
# ==================================

import layout_swe as keyboard_layout
#import layout_uk as keyboard_layout

# ==================================
```

In this case, the `swe` layout is chosen. To switch to the UK layout instead, comment out the line with `swe` in it and uncomment the line with `uk` in it, like this:

```python
# Choose your layout here
# ==================================

#import layout_swe as keyboard_layout
import layout_uk as keyboard_layout

# ==================================
```

> [!WARNING] Be sure to only select one layout at a time!
> If you for example had left the code like this:
>
> ```python
> # Choose your layout here
> # ==================================
> 
> import layout_swe as keyboard_layout
> import layout_uk as keyboard_layout
> 
> # ==================================
> ```
> ... then the layout that is last in the list will override the layout before it, and you might not end up with the result you expect.
