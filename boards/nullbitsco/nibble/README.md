Keyboard mapping for the [nullbits nibble](https://nullbits.co/nibble/).

Copy `kb.py` and `main.py` to your top level CircuitPython folder beside the kmk folder.
Edit the key mapping in `main.py` to match your keyboard layout.

The Keyboard constructor supports a couple of optional arguments (see `kb.py`).

TODO

You can specify the active encoder positions by passing a list like
`active_encoders=[0, 2]` which corresponds to the 1st and 3rd positions shown
in [step 6](https://github.com/nullbitsco/docs/blob/main/tidbit/build_guide_en.md#6-optional-solder-rotary-encoder-led-matrix-andor-oled-display) of the build guide.
The default is for a single encoder in either of the top two locations labeled 1
in the build diagram, i.e. `active_encoders=[0]`.  Pass an empty list if you skipped
adding any encoders.

You can control the RGB backlights with the [RGB extension](http://kmkfw.io/docs/rgb).
Here's an example:

```python
from kb import KMKKeyboard
from kmk.extensions.rgb import RGB, AnimationModes

keyboard = KMKKeyboard(active_encoders=[0])

rgb = RGB(
    pixel_pin=keyboard.pixel_pin,
    num_pixels=10,
    animation_mode=AnimationModes.BREATHING,
    animation_speed=3,
    breathe_center=2,
)
keyboard.extensions.append(rgb)

```
