# Oled Display
More user friendly extension than PEG Oled for using OLED display in your build.

If you need help soldering, there's a small note on the end to help.

# Preparation

### Libraries
First of all you need to download few Libraries that will make possible for your OLED to work. You can download them from Adafruit CircuitPython Libraries page. 
#### Make sure you download right version of Libraries. It should be the same one as yours CircuitPyhon.
* [CircuitPython Libraries Bundle](https://circuitpython.org/libraries)

Now you need to create `lib` folder where you will place your needed files.
Then find following folder and file and drop them in your freshly baked folder.
* adafruit_display_text
* `adafruit_displayio_ssd1306.mpy`

# Main.py
Time to make changes in your `main.py`.
As always, first step is adding OLED extension.

```python
from kmk.extensions.oled import Oled, TextEntry, ImageEntry
```

Now add this main part of extension. Then replace SCL and SDA. You can also tweak some settings of your screen here, but for now its not necessary.

```python
i2c_bus = busio.I2C(board.GP SCL, board.GP SDA) # change SCL and SDA according to your board and made connection.
oled = Oled(
    i2c=i2c_bus,
    device_address=0x3C,
    height=64, # here you can change your screen size
    flip=False,
    dim_time=10,
    dim_target=0.1, 
    off_time=0, 
    brightness=0.1,
    brightness_step=0.1,
)
```
### All set.
You just need to add few lines of code, depending if you want to display text or images.

I'll start with second one as its slight easier.

# Image

Before starting make sure you got a ready file to display. It should be a monochromatic bitmap (for example `1.bmp`) with same size as your's OLED. In this case 128x64. 
Place your image straight into your CircuitPython file, next to `main.py`. 
#### Placing it in separate folder may cause issues.

```python
oled.entries = [
    ImageEntry(image="1.bmp", x=0, y=0),
]
keyboard.extensions.append(oled)
```

You can also make your images appear corresponding to specific layer or side of your split keyboard

```python
oled.entries = [
    ImageEntry(image="1.bmp", x=0, y=0, layer=0),
    ImageEntry(image="2.bmp", x=0, y=0, layer=1),
    ImageEntry(image="L1.bmp", x=0, y=0, layer=3, side="L"),
    ImageEntry(image="R1.bmp", x=0, y=0, layer=3, side="R"),
]
keyboard.extensions.append(oled)
```

# Text
Displaying text is also really easy and gives you more settings to tweak around.

```python
oled.entries = [
    TextEntry(text="Layer = 1", x=0, y=0, direction='LTR', line_spacing=0.75),
    TextEntry(text="Macros", x=0, y=12, direction='LTR', line_spacing=0.75),
    TextEntry(text="Hey there!", x=0, y=24, direction='LTR', line_spacing=0.75),
]
keyboard.extensions.append(oled)
```

To display longer texts you need to divide it to smaller phrases to fit width of your screen.
You're able to freely change line spacing and positon of your text to place it wherever you want.
As well as with images you can change displaying according to your layer or side of split keyboard.

```python
oled.entries = [
    TextEntry(text="Inverted", x=0, y=0, direction='LTR', inverted=True, line_spacing=0.75, layer=0),
    TextEntry(text="Left", x=0, y=12, direction='LTR', line_spacing=0.75, layer=0, side="L"),
    TextEntry(text="Right", x=0, y=24, direction='LTR', line_spacing=0.75, layer=0, side="R"),
]
keyboard.extensions.append(oled)
```

# Soldering

Look online for your board pinout docs and solder accordingly to it.

[Raspberry Pi Pico Pinouts](https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg)

* GND - Ground Pin
* VCC - 3V3 Pin
* SCL - any SCL pin 
* SDA - closest SDA pin
