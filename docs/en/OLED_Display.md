# OLED Display
Extension to use for your build with OLED Display.

## Preparation

### Libraries
First of all you need to download a few libraries that will make it possible for your OLED to work.\
Make sure you download right version of Libraries. It should be the same one as yours CircuitPyhon.\
You can get them with the [Adafruit CircuitPython Libraries bundle](https://circuitpython.org/libraries).

Now you need to create a `lib` folder where you will place your needed files.\
Then find following folder and file and drop them in your freshly baked folder.
* `adafruit_display_text`
* `adafruit_displayio_ssd1306.mpy`

## Configuration
Time to make changes in `main.py`.\
As always, first step is adding OLED extension as well as busio and board.

```python
import board
import busio
from kmk.extensions.oled import Oled, TextEntry, ImageEntry
```

Now add this main part of extension. Then replace `SCL` and `SDA` with correct pins.\
Here you will also find the main section with all the settings that you can customize according to your screen and preferences.

```python
i2c_bus = busio.I2C(board.GP SCL, board.GP SDA) # change SCL and SDA according to your board and made connection.

oled = Oled(
    i2c=i2c_bus,
    device_address=0x3C,
    width=128, # screen size
    height=64, # screen size
    flip = False, # flips your display content
    flip_left = False, # flips your display content on left side split
    flip_right = False, # flips your display content on right side split
    dim_time=10, # time in seconds to reduce screen brightness
    dim_target=0.1, # set level for brightness decrease
    off_time=0, # time in seconds to turn off screen
    brightness=1, # initial screen brightness level
    brightness_step=0.1, # used for brightness increase/decrease keycodes
    # POWER SAVE ONLY SETTINGS
    powersave_dim_time=10, # time in seconds to reduce screen brightness
    powersave_dim_target=0.1, # set level for brightness decrease
    powersave_off_time=30, # time in seconds to turn off screen
)
```

## Images

Before starting make sure you got a ready file to display.\
It should be a monochromatic bitmap with same size as your's OLED. In this case 128x64.\
Place your image straight into your CircuitPython file, next to `main.py`.\
**Placing it in separate folder may cause issues.**

```python
oled.entries = [
    ImageEntry(image="1.bmp", x=0, y=0),
]
keyboard.extensions.append(oled)
```

You can also make your images appear corresponding to specific layer.

```python
oled.entries = [
    ImageEntry(image="1.bmp", x=0, y=0, layer=0),
    ImageEntry(image="2.bmp", x=0, y=0, layer=1),
]
keyboard.extensions.append(oled)
```

And/or side of your split keyboard.

```python
oled.entries = [
    ImageEntry(image="L1.bmp", x=0, y=0, side="L"),
    ImageEntry(image="R1.bmp", x=0, y=0, side="R"),
]
keyboard.extensions.append(oled)
```

## Text
You're able to freely positon your text to place it wherever you want just by changing x and y values.

```python
oled.entries = [
    TextEntry(text="Layer = 1", x=0, y=0),
    TextEntry(text="Macros", x=0, y=12),
    TextEntry(text="Hey there!", x=0, y=24),
]
keyboard.extensions.append(oled)
```
### X and Y anchors
It's helpfull with positioning of text.\
The values can be set `T` for Top, `M` for Middle and `B` for Bottom for X axis as well as `L` for Left, `M` for Middle and `R` for Right for Y axis.

It sets the anchor point of the given text, and the text is moved and placed based on this anchor point.\
For example for text in top right corner you need to set its anchor points Top Right and move text to far right position.

For some more info about anchors check [Adafruit site](https://learn.adafruit.com/circuitpython-display-support-using-displayio/text). But keep in mind that KMK operates with `T`, `M`,`B` and `L`, `M`, `R` strings, not numbers.

```python
oled.entries = [
    TextEntry(text="Layer = 1", x=128, y=0, x_anchor="R", y_anchor="T"), # text in Top Right corner
    TextEntry(text="Macros", x=128, y=64, x_anchor="R", y_anchor="B"), # text in Bottom Right corner
    TextEntry(text="Hey there!", x=64, y=32, x_anchor="M", y_anchor="M"), # text in the Middle of screen
]
keyboard.extensions.append(oled)
```

### Split
As well as with images you can change displaying according to your layer or side of split keyboard.

```python
oled.entries = [
    TextEntry(text="Longer text that", x=0, y=0, layer=0),
    TextEntry(text="has been divided", x=0, y=12, layer=0, side="L"),
    TextEntry(text="for an example", x=0, y=24, layer=0, side="R"),
]
keyboard.extensions.append(oled)
```

### Inverting
Inverts colours of your text. Comes in handy, for example, as a good layer indicator.

```python
oled_ext = Oled(
    entries=[
        TextEntry(text='0 1 2 4', x=0, y=0),
        TextEntry(text='0', x=0, y=0, inverted=True, layer=0),
        TextEntry(text='1', x=12, y=0, inverted=True, layer=1),
        TextEntry(text='2', x=24, y=0, inverted=True, layer=2),
    ],
)
```

# Example Code

```python
import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.extensions.oled import Oled, TextEntry, ImageEntry

#EXTENSIONS
keyboard = KMKKeyboard()
Layers = Layers()
keyboard.modules.append(Layers)


#OLED
keyboard.SDA = board.GP20
keyboard.SCL = board.GP21
i2c_bus = busio.I2C(board.GP21, board.GP20)
oled = Oled(
    entries=[
        TextEntry(text='Layer: ', x=0, y=32, y_anchor='B'),
        TextEntry(text='BASE', x=40, y=32, y_anchor='B', layer=0),
        TextEntry(text='NUM', x=40, y=32, y_anchor='B', layer=1),
        TextEntry(text='NAV', x=40, y=32, y_anchor='B', layer=2),
        TextEntry(text='0 1 2', x=0, y=4),
        TextEntry(text='0', x=0, y=4, inverted=True, layer=0),
        TextEntry(text='1', x=12, y=4, inverted=True, layer=1),
        TextEntry(text='2', x=24, y=4, inverted=True, layer=2),
    ],
    i2c=i2c_bus,
    device_address=0x3C,
    width=128,
    height=64,
    dim_time=10,
    dim_target=0.1,
    off_time=1200,
    brightness=1,
)

keyboard.extensions.append(oled)
```
