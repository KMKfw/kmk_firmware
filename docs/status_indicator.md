# Status Indicator
This extension allow you to customize reaction to layer and hid changes (capslock/ver-num/..). It provides only the kmk internal handling and makes no hardware assumption. This part is up to you so that this extension will be compatible with leds, neopixels, lcd or even servo !

This extension is then for you if you want to act on your keyboard hardware on layer change. Other extensions can do that but assume certain hardware. Check if you are in one of those case:
- [Status LED](extension_statusled.md) for several, individual leds (a gpio per led).
- [Peg Oled Display](peg_oled_display.md) for oled display.

## How to use

You need to subclass `Indicator` and add your hardware setup in `__init__()` and customize the `update()` method.

Here is a simple example using a neopixel strip to set a color for each layers, and one for capslock (caplock being higher priority):

```python
import board
from kmk.extensions.status_indicator import Indicator
from kmk.kmk_keyboard import KMKKeyboard
from neopixel import NeoPixel


class MyIndicator(Indicator):
    # base layer -> off, layer 1 -> blue, layer 2 -> red
    LAYERS_COLORS = [(0, 0, 0), (0, 255, 0), (255, 0, 0)]
    CAPS_COLOR = (128, 128, 128)  # white

    def __init__(self, pixel_pin, num_pixels):
        super().__init__()  # Needed !
        self.np = NeoPixel(pixel_pin, num_pixels)

    def update(self):
        if self.get_caps_lock():
            # caps lock on:
            self.np.fill(self.CAPS_COLOR)
        else:
            self.np.fill(self.LAYERS_COLORS[self.layers[0]])

    def on_powersave_enable(self, sandbox):
        # turn off neopixel
        self.np.fill((0, 0, 0))

    def on_powersave_disable(self, sandbox):
        # restore neopixel
        self.update()


keyboard = KMKKeyboard()

my_indicator = MyIndicator(board.D4, 6)
keyboard.extensions.append(my_indicator)
```

## Available options

### Lock Status
As shown in the above example, you can use all the method of the [LockStatus](lock_status.md) Extension.

### Layers
You can use `self.layers` who is a list of all the currently enabled layers. The first element is the active layers. Most user will be happy only with this active layer indication but all layers are available if you want to use them. One might want to display a gradient of the respective layers colors on a neopixel strip for example, or show the full list on a oled screen...

### Key interaction
Remember, you can define custom key to interact with your extensions. A classic example would be to change the brightness of leds. Here is how to have a key that will cycle througt 4 different level:

```python
from kmk.keys import make_key
from kmk.extensions.status_indicator import Indicator

class MyIndicator(Indicator):
    def __init__(self, ...):
        ...

        self.brightness_level = 0
        make_key(names=('LED_LVL',), on_press=self._led_level)

    def _led_level(self)
        self.brightness_level = (self.brighteness_level + 1) % 4

    def update():
        # Up to you to use self.brightness_level in this function
        ...
```
