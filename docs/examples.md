# Examples
Here you can find some examples of what some users have created in their personal keyboard configs. These are here to
help you understand how some of the tools may be used.

## Changing LED color based on layers
This allows you to create a layer key that also changes colors when pushing a layer key, and restore turn off the lights
when you release the layer key. The example uses the MO though any layer switch keys can be used if imported. Just use the
LAYER_1 key in your keymap, and it's ready to go! You can change animations, colors, or anything in there.

```python
from kmk.handlers.layers import (mo_pressed, mo_released)
from kmk.keys import KC, layer_key_validator, make_argumented_key


def layer1p(*args, **kwargs):
    keyboard.pixels.set_hsv_fill(100, 100, 100)
    return mo_pressed(*args, **kwargs)


def layer1r(*args, **kwargs):
    keyboard.pixels.set_hsv_fill.fill(0, 0, 0)
    return mo_released(*args, **kwargs)
   
make_argumented_key(
    validator=layer_key_validator,
    names=('LAYER_1',),
    on_press=layer1p,
    on_release=layer1r,
)

LAYER_1 = KC.LAYER_1(1)

```