import board
import busio

from adafruit_mcp230xx.mcp23017 import MCP23017

from kmk.hid import HIDModes
from kmk.keys import KC
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.layers import Layers
from kmk.scanners import DiodeOrientation

# DEBUG_ENABLE = True

i2c = busio.I2C(scl=board.SCL, sda=board.SDA, frequency=100000)
mcp = MCP23017(i2c, address=0x20)
keyboard = KMKKeyboard()
layer = Layers
keyboard.modules = [layer]

_______ = KC.TRNS
XXXXXXX = KC.NO

FN = KC.MO(1)

keyboard.debug_enabled = True

keyboard.col_pins = (
    mcp.get_pin(8),
    mcp.get_pin(9),
    mcp.get_pin(10),
    mcp.get_pin(11),
    mcp.get_pin(12),
    mcp.get_pin(13),
    mcp.get_pin(14),
    mcp.get_pin(15),
    mcp.get_pin(4),
    mcp.get_pin(5),
    mcp.get_pin(6),
    mcp.get_pin(7),
    mcp.get_pin(3),
    mcp.get_pin(2),
    mcp.get_pin(1),
)
keyboard.row_pins = (board.D7, board.D6, board.D5, board.D3, board.D2)
keyboard.diode_orientation = DiodeOrientation.COLUMNS

# fmt:off
keyboard.keymap = [
    # Qwerty
    # ,--------------------------------------------------------------------------------------------------------.
    # |   `  |   1  |   2  |   3  |   4  |   5  |   6  |   7  |   8  |   9  |   0  |   -  |   =  | Bksp | Del  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Tab  |   Q  |   W  |   E  |   R  |   T  |   Y  |   U  |   I  |   O  |   P  |   [  |   ]  |   \  | PgUp |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------+------|
    # | Esc  |   A  |   S  |   D  |   F  |   G  |   H  |   J  |   K  |   L  |   ;  |   '  |      |Enter | PgDn |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Shift|   Z  |   X  |   C  |   V  |   B  |   N  |   M  |   ,  |   .  |   /  |Shift |      |  Up  | Ins  |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Ctrl | GUI |  Alt  |      |      |Space |      |      |  Fn  | Alt  | Ctrl | Left |      | Down | Right|
    # `------------------------------------------------------------------------------------------+------+------'
    [
        KC.GRV,  KC.N1,   KC.N2,   KC.N3,   KC.N4,     KC.N5,   KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.MINS, KC.EQUAL, KC.BSPC,   KC.DEL,
        KC.TAB,  KC.Q,    KC.W,    KC.E,    KC.R,      KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.LBRC, KC.RBRC,  KC.BSLASH, KC.PGUP,
        KC.ESC,  KC.A,    KC.S,    KC.D,    KC.F,      KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.QUOT, XXXXXXX,  KC.ENTER,  KC.PGDN,
        KC.LSFT, KC.Z,    KC.X,    KC.C,    KC.V,      KC.B,    KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.RSFT, XXXXXXX,  KC.UP,     KC.INS,
        KC.LCTL, KC.LGUI, KC.LALT, XXXXXXX, XXXXXXX,   KC.SPC,  XXXXXXX, XXXXXXX, FN,      KC.RALT, KC.RCTL, KC.LEFT, XXXXXXX,  KC.DOWN,   KC.RIGHT,
    ],


    # Functions
    # ,--------------------------------------------------------------------------------------------------------.
    # |      |  F1  |  F2  |  F3  |  F4  |  F5  |  F6  |  F7  |  F8  |  F9  |  F10 |  F11 |  F12 |      | CLR* |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Tab  |      |      |      |      |      |      |      |      |Print |      |Pause | Calc |      | BrUp |
    # |------+------+------+------+------+-------------+------+------+------+------+------+------+------+------|
    # | Esc  |      |      |      |      |      |      |      |      |      |      |      |      |      | BrDn |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Shift|      | Play | Stop | Prev | Next | VolDn| VolUp| Mute |      |      |Shift |      |LedUp |      |
    # |------+------+------+------+------+------+------+------+------+------+------+------+------+------+------|
    # | Ctrl | GUI |  Alt  |      |      |Space |      |      |  Fn  | Alt  | Ctrl | BTPrv|      |LedDn | BTNxt|
    # `------------------------------------------------------------------------------------------+------+------'
    # CLR: Clear bonds
    [
        XXXXXXX, KC.F1,   KC.F2,   KC.F3,   KC.F4,    KC.F5,   KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,  KC.F11,    KC.F12,  XXXXXXX, KC.BT_CLR,
        KC.TAB,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, KC.PSCR, XXXXXXX, KC.PAUSE,  _______, XXXXXXX, _______,
        KC.ESC,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,  XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX, XXXXXXX,   XXXXXXX, XXXXXXX, _______,
        KC.LSFT, XXXXXXX, KC.MPLY, KC.MSTP, KC.MPRV,  KC.MNXT, KC.VOLD, KC.VOLU, KC.MUTE, XXXXXXX, XXXXXXX, KC.RSFT,   XXXXXXX, _______, XXXXXXX,
        KC.LCTL, KC.LGUI, KC.LALT, XXXXXXX, XXXXXXX,  KC.SPC,  XXXXXXX, XXXXXXX, FN,      KC.RALT, KC.RCTL, KC.BT_PRV, XXXXXXX, _______, KC.BT_NXT,
    ],
]
# fmt:on

if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE, ble_name='Lab68')
    # keyboard.go(hid_type=HIDModes.USB)
