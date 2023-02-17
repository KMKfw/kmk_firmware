# Pimoroni Trackball

Module handles usage of Trackball Breakout by Pimoroni.

Product page: https://shop.pimoroni.com/products/trackball-breakout

### Usage

Declare I2C bus and add this module in your main class.

```python
from kmk.modules.pimoroni_trackball import Trackball, TrackballMode
import busio as io

i2c = io.I2C(scl=board.D3, sda=board.D2)
trackball = Trackball(i2c)
keyboard.modules.append(trackball)
```

Module will also work when you cannot use `busio` and do `import bitbangio as io` instead.

### Key inputs, other handler combinations

If you have used this thing on a mobile device, you will know it excels at cursor movement

```python

from kmk.modules.pimoroni_trackball import Trackball, TrackballMode, PointingHandler, KeyHandler, ScrollHandler, ScrollDirection

trackball = Trackball(
    i2c, 
    mode=TrackballMode.MOUSE_MODE, 
    # optional: set rotation angle of the trackball breakout board, default is 1
    angle_offset=1.6, 
    handlers=[
        # act like an encoder, input arrow keys
        KeyHandler(KC.UP, KC.RIGHT, KC.DOWN, KC.LEFT, KC.ENTER), 
        # on layer 1 and above use the default pointing behavior
        PointingHandler(),
        # use ScrollDirection.NATURAL (default) or REVERSE to change the scrolling direction
        ScrollHandler(scroll_direction=ScrollDirection.NATURAL)
    ]
)

# now you can use these KeyCodes:

KC.TB_NEXT_HANDLER # rotates through available 
KC.TB_HANDLER(0) # activate KeyHandler 
KC.TB_HANDLER(1) # activate MouseHandler

```


### Backlight

Setup backlight color using below commands:

```python
trackball.set_rgbw(r, g, b, w)
trackball.set_red(brightness)
trackball.set_green(brightness)
trackball.set_blue(brightness)
trackball.set_white(brightness)
```

This module exposes one keycode `TB_MODE`, which on hold switches between `MOUSE_MODE` and `SCROLL_MODE`.
To choose the default mode, pass it in `Trackball` constructor.