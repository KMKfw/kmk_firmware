from kb import KMKKeyboard
from kmk.keys import KC
from kmk.extensions.rgb import RGB, AnimationModes
from kmk.extensions.media_keys import MediaKeys


keyboard = KMKKeyboard(encoder=True)    # assume encoder installed
keyboard.extensions.append(MediaKeys())

XXXXX = KC.NO

keyboard.keymap = [
    [
        XXXXX,  KC.ESC, KC.N1,  KC.N2,  KC.N3,  KC.N4,  KC.N5,  KC.N6,  KC.N7,  KC.N8,  KC.N9,  KC.N0,  KC.MINS,KC.EQL, KC.BKSP,KC.DEL,
        KC.MUTE,KC.TAB, KC.Q,   KC.W,   KC.E,   KC.R,   KC.T,   KC.Y,   KC.U,   KC.I,   KC.O,   KC.P,   KC.LBRC,KC.RBRC,KC.BSLS,KC.GRV,
        KC.F1,  KC.CAPS,KC.A,   KC.S,   KC.D,   KC.F,   KC.G,   KC.H,   KC.J,   KC.K,   KC.L,   KC.SCLN,KC.QUOT,KC.ENT, KC.ENT, KC.PGUP,
        KC.F2,  KC.LSFT,KC.Z,   KC.X,   KC.C,   KC.V,   KC.B,   KC.N,   KC.M,   KC.COMM,KC.DOT, KC.SLSH,KC.RSFT,XXXXX,  KC.UP,  KC.PGDN,
        KC.F3,  KC.LCTL,KC.LCMD,KC.LALT,KC.SPC, KC.SPC, KC.SPC, KC.SPC, KC.SPC, KC.RCMD,KC.RALT,KC.RCTL,KC.LEFT,XXXXX,  KC.DOWN,KC.RGHT,
    ]
]

# note that encoder button is configured in the keymap (KC.MUTE above) so set to XXXXX here
keyboard.encoders.map = [
    ( ( KC.VOLD, KC.VOLU, XXXXX),  ), # Layer 1, encoder 1
]

rgb = RGB(
    pixel_pin=keyboard.pixel_pin,
    num_pixels=10,
    animation_mode=AnimationModes.BREATHING,
    animation_speed=3,
    breathe_center=2,
)

keyboard.extensions.append(rgb)


def set_backlight(hsv):
    rgb.hue, rgb.sat, rgb.val = hsv


set_backlight((180,255,50))

if __name__ == '__main__':
    keyboard.go()
