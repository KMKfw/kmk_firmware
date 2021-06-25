from kb import KMKKeyboard
from kmk.extensions.rgb import RGB
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide, SplitType

keyboard = KMKKeyboard()

rgb_ext = RGB(pixel_pin=keyboard.rgb_pixel_pin, num_pixels=keyboard.rgb_num_pixels)
layers_ext = Layers()
# TODO Comment one of these on each side
split_side = SplitSide.LEFT
split_side = SplitSide.RIGHT
split = Split(split_type=SplitType.BLE, split_side=split_side)

keyboard.extensions = [rgb_ext]
keyboard.modules = [layers_ext, split]

_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(3)
RAISE = KC.MO(4)
ADJUST = KC.MO(5)

keyboard.keymap = [
    # Qwerty
    # ,-----------------------------------------------------------------------------------.
    # | Tab  |   Q  |   W  |   E  |   R  |   T  |   Y  |   U  |   I  |   O  |   P  | Bak  |
    # |------+------+------+------+------+-------------+------+------+------+------+------|
    # | Esc  |   A  |   S  |   D  |   F  |   G  |   H  |   J  |   K  |   L  |   ;  |  "   |
    # |------+------+------+------+------+------|------+------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   N  |   M  |   ,  |   .  |   /  |Enter |
    # |------+------+------+------+------+------+------+------+------+------+------+------|
    # |Adjust| Ctrl | Alt  | GUI  |Lower |Space |Space |Raise | Left | Down |  Up  |Right |
    # `-----------------------------------------------------------------------------------'
    [
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.BSPC,
        KC.GESC, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT,
        ADJUST,  KC.LCTL, KC.LALT, KC.LGUI, LOWER,   KC.SPC,  KC.SPC,  RAISE,   KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,
    ],

    # Colemak
    # ,-----------------------------------------------------------------------------------.
    # | Tab  |   Q  |   W  |   F  |   P  |   G  |   J  |   L  |   U  |   Y  |   ;  | Bak  |
    # |------+------+------+------+------+-------------+------+------+------+------+------|
    # | Esc  |   A  |   R  |   S  |   T  |   D  |   H  |   N  |   E  |   I  |   O  |  "   |
    # |------+------+------+------+------+------|------+------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   K  |   M  |   ,  |   .  |   /  |Enter |
    # |------+------+------+------+------+------+------+------+------+------+------+------|
    # |Adjust| Ctrl | Alt  | GUI  |Lower |Space |Space |Raise | Left | Down |  Up  |Right |
    # `-----------------------------------------------------------------------------------'
    [
        KC.TAB,  KC.Q,    KC.W,    KC.F,    KC.P,    KC.G,    KC.J,    KC.L,    KC.U,    KC.Y,    KC.SCLN, KC.BSPC,
        KC.GESC, KC.A,    KC.R,    KC.S,    KC.T,    KC.D,    KC.H,    KC.N,    KC.E,    KC.I,    KC.O,    KC.QUOT,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,    KC.K,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.ENT,
        ADJUST,  KC.LCTL, KC.LALT, KC.LGUI, LOWER,   KC.SPC,  KC.SPC,  RAISE,   KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,
    ],

    # Dvorak
    # ,-----------------------------------------------------------------------------------.
    # | Tab  |   "  |   ,  |   .  |   P  |   Y  |   F  |   G  |   C  |   R  |   L  | Bak  |
    # |------+------+------+------+------+-------------+------+------+------+------+------|
    # | Esc  |   A  |   O  |   E  |   U  |   I  |   D  |   H  |   T  |   N  |   S  |  /   |
    # |------+------+------+------+------+------|------+------+------+------+------+------|
    # | Shift|   ;  |   Q  |   J  |   K  |   X  |   B  |   M  |   W  |   V  |   Z  |Enter |
    # |------+------+------+------+------+------+------+------+------+------+------+------|
    # |Adjust| Ctrl | Alt  | GUI  |Lower |Space |Space |Raise | Left | Down |  Up  |Right |
    # `-----------------------------------------------------------------------------------'
    [
        KC.TAB,  KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,    KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.BSPC,
        KC.GESC, KC.A,    KC.O,    KC.E,    KC.U,    KC.I,    KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.SLSH,
        KC.LSFT, KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,    KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.ENT,
        ADJUST,  KC.LCTL, KC.LALT, KC.LGUI, LOWER,   KC.SPC,  KC.SPC,  RAISE,   KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT,
    ],

    # Lower
    # ,-----------------------------------------------------------------------------------.
    # |   ~  |   !  |   @  |   #  |   $  |   %  |   ^  |   &  |   *  |   (  |   )  | Del  |
    # |------+------+------+------+------+-------------+------+------+------+------+------|
    # | Del  |  F1  |  F2  |  F3  |  F4  |  F5  |  F6  |   .  |   +  |     |    \  |  |   |
    # |------+------+------+------+------+------|------+------+------+------+------+------|
    # |      |  F7  |  F8  |  F9  |  F10 |  F11 |  F12 |ISO ~ |ISO | |      |      |Enter |
    # |------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |             |      | Next | Vol- | Vol+ | Play |
    # `-----------------------------------------------------------------------------------'
    [
        KC.TILD, KC.EXLM, KC.AT,   KC.HASH, KC.DLR,  KC.PERC, KC.CIRC, KC.AMPR, KC.ASTR, KC.LPRN, KC.RPRN, KC.DEL,
        KC.DEL,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.UNDS, KC.PLUS, KC.LCBR, KC.RCBR, KC.PIPE,
        _______, KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.NUHS, KC.NUBS, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY,
    ],

    # Raise
    # ,-----------------------------------------------------------------------------------.
    # |   `  |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  | Del  |
    # |------+------+------+------+------+-------------+------+------+------+------+------|
    # | Del  |  F1  |  F2  |  F3  |  F4  |  F5  |  F6  |   -  |   =  |   [  |   ]  |  \   |
    # |------+------+------+------+------+------|------+------+------+------+------+------|
    # |      |  F7  |  F8  |  F9  |  F10 |  F11 |  F12 |ISO # |ISO / |      |      |Enter |
    # |------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |             |      | Next | Vol- | Vol+ | Play |
    # `-----------------------------------------------------------------------------------'
    [
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        KC.DEL,  KC.F1,   KC.F2,   KC.F3,   KC.F4,   KC.F5,   KC.F6,   KC.MINS, KC.EQL,  KC.LBRC, KC.RBRC, KC.BSLS,
        _______, KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,  KC.F12,  KC.NUHS, KC.NUBS, _______, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, KC.MNXT, KC.VOLD, KC.VOLU, KC.MPLY,
    ],

    # Adjust
    #  ,-----------------------------------------------------------------------------------.
    # |      | Reset|RGB Tg|RGB Md|Hue Up|Hue Dn|Sat Up|Sat Dn|Val Up|Val Dn|      |  Del |
    # |------+------+------+------+------+-------------+------+------+------+------+------|
    # |      |      |      |      |      |      |      |Qwerty|Colemk|Dvorak|      |      |
    # |------+------+------+------+------+------|------+------+------+------+------+------|
    # |      |      |      |      |      |      |      |      |      |      |      |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------|
    # |      |      |      |      |      |             |      |      |      |      |      |
    # `-----------------------------------------------------------------------------------'
    [
        _______, _______, KC.RGB.TOG, KC.RGB.MOD, KC.RGB.HUD, KC.RGB.HUI, KC.RGB.SAD, KC.RGB.SAI, KC.RGB.VAD, KC.RGB.VAI, _______, KC.DEL,
        _______, _______, _______,    _______,    _______,    _______,    _______,    KC.DF(0),   KC.DF(1),   KC.DF(2),   _______, _______,
        _______, _______, _______,    _______,    _______,    _______,    _______,    _______,    _______,    _______,    _______, _______,
        _______, _______, _______,    _______,    _______,    _______,    _______,    _______,    _______,    _______,    _______, _______,
    ],

]

if __name__ == '__main__':
    keyboard.go()
