# Pimoroni Trackball

Module handles usage of Trackball Breakout by Pimoroni.

## Usage

Declare I2C bus and add this module in your main class.

```python
from kmk.modules.pimoroni_trackball import Trackball, TrackballMode
import busio as io

i2c = io.I2C(scl=board.D3, sda=board.D2)
trackball = Trackball(i2c)
keyboard.modules.append(trackball)
```

Module will also work when you cannot use `busio` and do `import bitbangio as io` instead.

## Key inputs, other handler combinations

### Builtin Handlers

There are a couple of builtin handlers for your convenience.
All parameters are show with their default values, optional parameters can be
omitted.

#### Pointing Handler

Plain pointing device, i.e. a mouse:

```python
PointingHandler(
    # optional:
    on_press=KC.MB_LMB,
)
```

#### Scroll Handler

Make the Trackball act as a 2D scroll wheel.
The default scroll direction is `NATURAL` and can be set to `ScrollDirection.REVERSE`
if the Apple behavior is preferred.

```python
ScrollHandler(
    # optional:
    scroll_direction=ScrollDirection.NATURAL,
    on_press=KC.MB_LMB,
)
```

#### Key Handler

Emit key presses instead of movement:

```python
KeyHandler(
    up,            # key for the up direction
    right,         # key for the right direction
    down,          # key for the down direction
    left,          # key for the left direction
    press,         # key for pressing the trackball
    # optional:
    axis_snap=.25, # diagonal quantization accuracy
    steps=8,       # amount of rotational angle for one key tap
)
```

#### Custom Handler Example

Here's an example for a custom handler that scrolls up and down, holds keys
for left and right, and press is middle mouse button:

```python
from kmk.modules.pimoroni_trackball import TrackballHandler

CustomHandler(TrackballHandler):
    def handle(self, keyboard, trackball, x, y, switch, state):
        if x > 0:
            keyboard.tap_key(KC.RIGHT)
        elif x < 0:
            keyboard.tap_key(KC.LEFT)

        if y != 0:
            AX.W.move(keyboard, y)

        if switch:
            keyboard.pre_process_key(KC.MB_MMB, is_pressed=state)
```

### Assigning Handlers
If you have used this thing on a mobile device, you will know it excels at cursor movement

```python

from kmk.modules.pimoroni_trackball import Trackball, TrackballMode, PointingHandler, KeyHandler, ScrollHandler, ScrollDirection

trackball = Trackball(
    i2c,
    mode=TrackballMode.MOUSE_MODE,
    # optional: set rotation angle of the trackball breakout board, default is 1
    angle_offset=1.6,
    handlers=[
        # act like an encoder, input arrow keys, enter when pressed
        KeyHandler(KC.UP, KC.RIGHT, KC.DOWN, KC.LEFT, KC.ENTER),
        # on layer 1 and above use the default pointing behavior, left click when pressed
        PointingHandler(),
        # use ScrollDirection.NATURAL (default) or REVERSE to change the scrolling direction, left click when pressed
        ScrollHandler(scroll_direction=ScrollDirection.NATURAL, on_press=KC.MB_LMB)
    ]
)

# now you can use these KeyCodes:

KC.TB_NEXT_HANDLER # rotates through available 
KC.TB_HANDLER(0) # activate KeyHandler 
KC.TB_HANDLER(1) # activate MouseHandler

```


## Backlight

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


### Light animation

The trackball has a RGB LED which can be controlled with the [RGB extension](http://kmkfw.io/docs/rgb).
Example of very slowly glowing led, almost seamlessly changing colors:

```python
# initiate the trackball and add the library for the trackball pixel buffer
from kmk.modules.pimoroni_trackball import TrackballPixel

# add rgb extension with animations
from kmk.extensions.rgb import RGB, AnimationModes

# pass the pixel buffer to the rgb extension and declare pixel pin None
pixels = TrackballPixel(trackball)

# set the rgb animation configuration to your taste
rgb = RGB(pixel_pin=None,
        num_pixels=1,
        pixels=pixels,
        hue_default=0,
        sat_default=255,
        val_default=255,
        hue_step=1,
        sat_step=0,
        val_step=0,
        animation_speed=0.5,
        animation_mode=AnimationModes.SWIRL,
        )

keyboard.extensions.append(rgb)
```
