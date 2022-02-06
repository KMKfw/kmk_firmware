# Pimoroni Trackball

Module handles usage of Trackball Breakout by Pimoroni.

Product page: https://shop.pimoroni.com/products/trackball-breakout

### Usage

Declare I2C bus and add this module in your main class.

```python
from kmk.modules.pimoroni_trackball import Trackball, TrackballMode
import busio as io

i2c = io.I2C(scl=board.D3, sda=board.D2)
trackball = Trackball(i2c, mode=TrackballMode.MOUSE_MODE)
keyboard.modules.append(trackball)
```

Module will also work when you cannot use `busio` and do `import bitbangio as io` instead.

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