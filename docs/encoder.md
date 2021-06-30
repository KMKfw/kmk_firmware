# Encoder
Add twist control to your keyboard! Volume, zoom, anything you want.

## Enabling the extension
The constructor takes a minimun of 3 arguments: a list of pad_a pins, a list of pad_b pins, 
and an encoder_map.  The encoder_map is modeled after the keymap and works the
same way. It shoul have as many layers as your keymap, and use filler keys for 
layers that you don't require any action.  The encoder supports a velocity mode
if you desire to make something for video or sound editing. The direction of 
increment/decrement can be changed to make sense for the direction the knob is 
turning by setting the is_inverted flag.

## Configuration
First, create the encoder_map.

Anatomy of an encoder_map tuple: (increment_key, decrement_key, keys presses per click)

Create your special keys:

Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)



encoder_map = [
    [
        (KC.VOLU,KC.VOLD,2),
    [
        (Zoom_in, Zoom_out,1),
    ],
    [
        (_______,_______,1),
    ]
]


Now create the module
'''
encoder_ext = EncoderHandler([board.D40],[board.D41], encoder_map)
'''

If needed, invert the know direction
'''
encoder_ext.encoders[0].is_inverted = True
'''

Now, add it to your modules list
'''
keyboard.modules = [layers_ext, encoder_ext]
'''
