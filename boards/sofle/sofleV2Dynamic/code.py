import board

from kb import KMKKeyboard
from sided import side

from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers as _Layers
from kmk.modules.split import Split, SplitType, SplitSide
import busio as io
import math

keyboard = KMKKeyboard()

split = Split(
    split_flip=True,  # If both halves are the same, but flipped, set this True
    split_type=SplitType.UART,  # Defaults to UART
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=board.RX,  # The primary data pin to talk to the secondary device with
    data_pin2=board.TX,  # Second uart pin to allow 2 way communication
    use_pio=True,  # allows for UART to be used with PIO
    split_side=side,
)
keyboard.modules = [_Layers(),  split]

if side == SplitSide.LEFT:
    colors = {
        'base': (0, 0, 0, 0),
        'qwerty': (127, 0, 0, 0),
        'dvorak': (0, 127, 0, 0),
        'symbols': (0, 0, 0, 127),
        'directions': (0, 0, 127, 0),
    }
    from kmk.modules.pimoroni_trackball import Trackball, TrackballMode, PointingHandler, KeyHandler, ScrollHandler, ScrollDirection
    print('detected left side')
    i2c = io.I2C(scl=board.D3, sda=board.D2)
    trackball = Trackball(i2c, mode=TrackballMode.MOUSE_MODE,
        angle_offset=math.radians(-90), handlers=[PointingHandler()])

    keyboard.modules.append(trackball)
    class Layers(_Layers):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            trackball.set_rgbw(*colors['base'])
        last_layer = 0
        def after_hid_send(self, keyboard):
            if keyboard.active_layers[0] != self.last_layer:
                if keyboard.debug_enabled:
                    print('layer swap from', self.last_layer, 'to', keyboard.active_layers[0])
                self.last_layer = keyboard.active_layers[0]
                newname = keyboard.layernames[self.last_layer]
                new_colors = colors[newname]
                if keyboard.debug_enabled:
                    print('setting colors to', new_colors, keyboard.layernames[self.last_layer])
                trackball.set_rgbw(*new_colors)
    keyboard.modules[0] = Layers()


# Cleaner key names
SYMB = "symbols"
SYMB_S = "symbols_default"
DIRS = "directions"
DIRS_S = "directions_default"
QWERTY = "qwerty"
QWERT_S = "qwerty_default"
DVORAK = "dvorak"
DVORA_S = "dvorak_default"
RESET = "base_only"


qwerty_dvorak = {
    KC.A: KC.A, KC.S: KC.O, KC.D: KC.E, KC.F: KC.U, KC.Q: KC.QUOT, KC.MINS: KC.RBRC,
    KC.T: KC.Y, KC.X: KC.Q, KC.C: KC.J, KC.V: KC.K, KC.W: KC.COMM, KC.LBRC: KC.SLSH,
    KC.U: KC.G, KC.I: KC.C, KC.O: KC.R, KC.P: KC.L, KC.Z: KC.SCLN, KC.QUOT: KC.MINS,
    KC.K: KC.T, KC.L: KC.N, KC.N: KC.B, KC.M: KC.M, KC.SCLN: KC.S, KC.DOT: KC.V,
    KC.Y: KC.F, KC.J: KC.H, KC.G: KC.I, KC.B: KC.X, KC.COMM: KC.W, KC.RBRC: KC.EQL,
    KC.H: KC.D, KC.R: KC.P, KC.E: KC.DOT,           KC.SLSH: KC.Z, KC.EQL: KC.RBRC,
}

base = [
    KC.TAB,  QWERT_S, KC.NO,   KC.NO,   KC.NO,   KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.BSPC,
    KC.ESC,  KC.NO,   KC.NO,   DVORA_S, KC.NO,   KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.ENT,
    KC.LSFT, KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.RSFT,
    KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.LALT, KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.DEL,
    KC.LGUI, KC.NO,   KC.LCTL, SYMB,    KC.SPC,  KC.TRNS,     KC.TRNS, KC.SPC,  SYMB,    KC.RCTL, KC.RALT, KC.RGUI,
]

# qwerty
qwerty = [
    KC.TRNS, KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,        KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.TRNS,
    KC.TRNS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,        KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.TRNS,
    KC.TRNS, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,        KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
]

# dvorak
dvorak = [
    KC.TRNS, KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,        KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.TRNS,
    KC.TRNS, KC.A,    KC.O,    KC.E,    KC.U,    KC.I,        KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.TRNS,
    KC.TRNS, KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,        KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
]

symbols = [
    RESET,   KC.NO,   KC.LPRN, KC.RPRN, KC.SLSH, KC.NO,       KC.NO,   KC.BSLS, KC.GRV,  KC.NO,   KC.NO,   KC.NO,
    DIRS_S,  KC.NO,   KC.LBRC, KC.RBRC, KC.PIPE, KC.PLUS,     KC.MINS, KC.EQL,  KC.UNDS, KC.NO,   KC.NO,   KC.NO,
    KC.TRNS, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,       KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.NO,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
]

# symbols = [
#     RESET,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.TRNS,
#     KC.TRNS, KC.LPRN, KC.RPRN, KC.UNDS, KC.LCBR, KC.RCBR,     KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.TRNS,
#     DIRS_S,  KC.LBRC, KC.RBRC, KC.SLSH, KC.PIPE, KC.BSLS,     KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.TRNS,
#     KC.TRNS, KC.QUOT, KC.DQUO, KC.PLUS, KC.MINS, KC.EQL,      KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.TRNS,
#     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
# ]

from kmk.handlers.sequences import simple_key_sequence
class VimFunctions:  # Vim Functions
    A = KC.NO # simple_key_sequence((KC.TG("disable current layer"), KC.END))
    B = KC.LCTL(KC.LEFT)
    C = KC.NO  # = cut and disable current layer
    D = KC.LCTL(KC.X)  # cut
    E = KC.NO  # = same as w?
    F = KC.NO  # don't think its possible
    G = KC.NO  # nope
    H = KC.NO  #
    H = KC.LEFT
    I = "directions_default"  # = disable current layer
    J = KC.DOWN
    K = KC.UP
    L = KC.RIGHT
    M = KC.NO  # not possible
    N = simple_key_sequence((KC.LCTL(KC.F), KC.ENT))
    O = simple_key_sequence((KC.END, KC.ENT))
    P = KC.LCTL(KC.V)  # paste
    Q = KC.NO  # should be able to record dynamic key sequence (along with the count before replaying)
    R = KC.LCTL(KC.Y)
    S = KC.NO  #
    T = KC.NO  #
    U = KC.LCTL(KC.Z)
    V = KC.NO  # hold shift
    W = KC.LCTL(KC.RIGHT)
    X = KC.DEL  # delete
    Y = KC.LCTL(KC.C)  # copy
    Z = KC.NO  # is leader
    SLSH = KC.LCTL(KC.F)
    TRNS = KC.TRNS

    def __getattr__(self, item):
        print(item)
        return KC.NO

    def __getitem__(self, item):
        print(item)
        if item == "TRNS":
            return KC.TRNS
        return KC.NO

VF = VimFunctions()

directions = [
    KC.TRNS, VF.QUOT, VF.COMM, VF.DOT,  VF.P,    VF.Y,        VF.F,    VF.G,    VF.C,    VF.R,    VF.L,    KC.TRNS,
    DIRS_S,  VF.A,    VF.O,    VF.E,    VF.U,    VF.I,        VF.D,    VF.H,    VF.T,    VF.N,    VF.S,    KC.TRNS,
    KC.TRNS, VF.SCLN, VF.Q,    VF.J,    VF.K,    VF.X,        VF.B,    VF.M,    VF.W,    VF.V,    VF.Z,    KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
]

def copy(layer):
    return [k for k in layer]

def invert(layer):
    rv = [None] * (5 * 12)
    def orig_to_new(n):
        x = n%12
        y = n // 12
        rv = y * 12 + (12 - x) - 1
        return rv
    for i, k in enumerate(layer):
        rv[orig_to_new(i)] = k
    return rv

def create_keymap(*layouts):
    # creates [layout 1, layout 2, ..., layout 1(reversed), layout 2(reversed), ...]
    rv = []
    layer_order = [l[0] for l in layouts]
    print('layers:', layer_order)
    def layer_index(name):
        return layer_order.index(name)
    def handle_custom_key(k):
        if k in layer_order:
            layername = k
            code = KC.MO
        elif k.endswith("_default"):
            layername = k[:-8]
            code = KC.TG
        elif k.endswith("_only"):
            layername = k[:-5]
            code = KC.TO
        else:
            raise ValueError("unrecognized string key:", k)
        return code(layer_index(layername))

    def add(layer, name):
        to_add = []
        print(f"adding layer {name}", end='')
        for i, k in enumerate(layer):
            if i%12 == 0:
                print('.', end='')
            if not isinstance(k, str):
                to_add.append(k)
            else:
                to_add.append(handle_custom_key(k))
        print(len(rv))
        rv.append(to_add)

    for name, l in layouts:
        add(l, name)

    return rv, layer_order

keyboard.keymap, keyboard.layernames = create_keymap(
    ("base", base),
    ("qwerty", qwerty),
    ("dvorak", dvorak),
    ("symbols", symbols),
    ("directions", directions)
)


print('keymap created')

if __name__ == '__main__':
    keyboard.active_layers = [0]
    keyboard.debug_enabled = True
    keyboard.go()
