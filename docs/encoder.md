# Encoder
Add twist control to your keyboard! Volume, zoom, anything you want.

## Enabling the extension
The constructor takes a minimun of 3 arguments: a list of pad_a pins, a list of pad_b pins, 
and an encoder_map.  The encoder_map is modeled after the keymap and works the
same way. It should have as many layers as your keymap, and use KC.NO keys for 
layers that you don't require any action.  The encoder supports a velocity mode
if you desire to make something for video or sound editing. The direction of 
increment/decrement can be changed to make sense for the direction the knob is 
turning by setting the is_inverted flag.

## Configuration

There is a complete example in the Atreus62 main.py

Create your special keys:
```python
Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)
```
Create the encoder_map.

Anatomy of an encoder_map tuple: (increment_key, decrement_key, keys presses per encoder click)

```python

# create the encoder map, modeled after the keymap
encoder_map = [
    [
        # Only 1 encoder is being used, so only one tuple per layer is required
        # Increment key is volume up, decrement key is volume down, and sends 2 
        # key presses for every "click" felt while turning the encoder.
        (KC.VOLU,KC.VOLD,2),
    [
        # only one key press sent per encoder click
        (Zoom_in, Zoom_out,1),
    ],
    [
        # No action keys sent here, the resolution is a dummy number, to be 
        # removed in the future.
        (_______,_______,1),#
    ]
]

# create the encoder instance, and pass in a list of pad a pins, a lsit of pad b 
# pins, and the encoder map created above
encoder_ext = EncoderHandler([board.D40],[board.D41], encoder_map)

# if desired, you can flip the incrfement/decrement direction of the knob by
# setting the is_inerted flag to True.  If you turn the knob to the right and 
# the volume goes down, setting this flag will make it go up.  It's default
# setting is False
encoder_ext.encoders[0].is_inverted = True

# Make sure to add the encoder_ext to the modules list
keyboard.modules = [encoder_ext]
```
