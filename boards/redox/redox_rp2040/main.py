import board
from kb import KMKKeyboard
from kmk.consts import UnicodeMode
from kmk.extensions.media_keys import MediaKeys
from kmk.keys import KC
from kmk.modules.holdtap import HoldTap
from kmk.modules.layers import Layers
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.split import Split, SplitSide, SplitType
from storage import getmount

keyboard = KMKKeyboard()
keyboard.debug_enabled = True
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.extensions.append(MediaKeys())
keyboard.modules.append(HoldTap())
keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())

split_side = SplitSide.RIGHT if str(getmount('/').label)[-1] == 'R' else SplitSide.LEFT

if split_side == SplitSide.LEFT:
    data_pin = board.GP0
    data_pin2 = board.GP1
else:
    data_pin = board.GP1
    data_pin2 = board.GP0

split = Split(
    split_side=split_side,
    split_target_left=False,
    split_type=SplitType.UART,
    split_flip=True,
    uart_interval=20,
    data_pin=data_pin,
    data_pin2=data_pin2,
    use_pio=True,
)
keyboard.modules.append(split)

XXXXX = KC.NO                       # Unmapped key
_____ = KC.TRNS                     # Transparent key

# Home row mods                      |PRESSED   |HOLD       |
AGUI = KC.HT(KC.A, KC.LGUI)  # |A         |GUI           |
SALT = KC.HT(KC.S, KC.LALT)  # |S         |ALT           |
DSFT = KC.HT(KC.D, KC.LSFT)  # |D         |SFT           |
FCTL = KC.HT(KC.F, KC.LCTRL)  # |F         |CTRL          |

JCTL = KC.HT(KC.J, KC.RCTRL)  # |J         |CTRL          |
KSFT = KC.HT(KC.K, KC.RSFT)  # |K         |SFT           |
LALT = KC.HT(KC.L, KC.RALT)  # |L         |ALT           |
CGUI = KC.HT(KC.SCLN, KC.RGUI)  # |;         |GUI           |

LT_MINS = KC.LT(2, KC.MINS)
LT_PGUP = KC.LT(3, KC.PGUP)
LT_END = KC.LT(3, KC.END)
LA_PAST = KC.HT(KC.PAST, KC.LALT)
LC_BSLS = KC.HT(KC.BSLS, KC.LCTL)

keyboard.keymap = [
    [
        # QWERTY
    # fmt: off
    #  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
        KC.ESC  ,KC.N1   ,KC.N2   ,KC.N3   ,KC.N4   ,KC.N5   ,KC.MINS ,                           KC.EQL  ,KC.N6   ,KC.N7   ,KC.N8   ,KC.N9   ,KC.N0   ,XXXXX   ,
    #  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
        KC.TAB  ,KC.Q    ,KC.W    ,KC.E    ,KC.R    ,KC.T    ,KC.LBRC ,                           KC.RBRC ,KC.Y    ,KC.U    ,KC.I    ,KC.O    ,KC.P    ,KC.BSLS ,
    #  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
        KC.LCAP ,AGUI    ,SALT    ,DSFT    ,FCTL    ,KC.G    ,                                             KC.H    ,JCTL    ,KSFT    ,LALT    ,CGUI    ,KC.QUOT ,
    #  |--------|--------|--------|--------|--------|--------|--------|--------|        |--------|--------|--------|--------|--------|--------|--------|--------|
        KC.LSFT ,KC.Z    ,KC.X    ,KC.C    ,KC.V    ,KC.B    ,KC.PGDN ,KC.PGUP ,         KC.HOME ,KC.END  ,KC.N    ,KC.M    ,KC.COMM ,KC.DOT  ,KC.SLSH ,KC.RSFT ,
    #  |--------|--------|--------|--------|--------|--------|--------|--------|        |--------|--------|--------|--------|--------|--------|--------|--------|
        KC.LGUI ,KC.PPLS ,KC.PMNS ,XXXXX   ,      XXXXX      ,KC.BSPC ,KC.DEL  ,         KC.ENT  ,KC.SPC  ,     KC.SPC      ,KC.LEFT ,KC.DOWN ,KC.UP   ,KC.RGHT ,
    #  |--------|--------|--------|--------|-----------------|--------|--------|        |--------|--------|-----------------|--------|--------|--------|--------|
    ],
    [
    # SYMB
    # fmt: off
    #  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
        KC.GRV  ,KC.F1   ,KC.F2   ,KC.F3   ,KC.F4   ,KC.F5   ,XXXXX   ,                           XXXXX   ,KC.F6   ,KC.F7   ,KC.F8   ,KC.F9   ,KC.F10  ,XXXXX   ,
    #  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
        _____   ,KC.EXLM ,KC.AT   ,KC.LCBR ,KC.RCBR ,KC.PIPE ,_____   ,                           _____   ,KC.PSLS ,KC.P7   ,KC.P8   ,KC.P9   ,KC.PMNS ,XXXXX   ,
    #  |--------|--------|--------|--------|--------|--------|--------|                          |--------|--------|--------|--------|--------|--------|--------|
        _____   ,KC.HASH ,KC.DLR  ,KC.LBRC ,KC.RBRC ,KC.GRV  ,                                             KC.PAST ,KC.P4   ,KC.P5   ,KC.P6   ,KC.PPLS ,XXXXX   ,
    #  |--------|--------|--------|--------|--------|--------|--------|--------|        |--------|--------|--------|--------|--------|--------|--------|--------|
        _____   ,KC.PERC ,KC.CIRC ,KC.LPRN ,KC.RPRN ,KC.TILD ,_____   ,_____   ,         _____   ,_____   ,XXXXX   ,KC.P1   ,KC.P2   ,KC.P3   ,KC.PENT ,XXXXX   ,
    #  |--------|--------|--------|--------|--------|--------|--------|--------|        |--------|--------|--------|--------|--------|--------|--------|--------|
        _____   ,_____   ,_____   ,_____   ,     _____       ,_____   ,_____   ,         _____   ,_____   ,     KC.RALT     ,KC.P0   ,KC.PDOT ,KC.PENT ,XXXXX   ,
    #  |--------|--------|--------|--------|-----------------|--------|--------|        |--------|--------|-----------------|--------|--------|--------|--------|
    ],

]

if __name__ == '__main__':
    keyboard.go()

