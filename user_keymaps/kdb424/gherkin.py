from kmk.consts import DiodeOrientation, UnicodeMode
from kmk.handlers.sequences import (compile_unicode_string_sequences,
                                    send_string)
from kmk.keys import KC
from kmk.mcus.circuitpython_samd51 import Firmware
from kmk.pins import Pin as P
from kmk.types import AttrDict

keyboard = Firmware()

'''
Converter/handwire:

PB5: SCL
PB4: SDA
PE6: A0
PD7: A1
PC6: A2
PD4: A3
PD0: A4

PB6: D2
PB2: TX
PB3: RX
PB1: MI
PF7: MO
PF6: SCK
PF5: A5

Mosfet on B5 to control backlight
'''

keyboard.col_pins = (P.A4, P.A2, P.A3, P.A1, P.A0, P.SDA)
keyboard.row_pins = (P.D2, P.TX, P.RX, P.MISO, P.MOSI)

# Kyle is fucking stupid
keyboard.col_pins = tuple(reversed(keyboard.col_pins))
keyboard.row_pins = tuple(reversed(keyboard.row_pins))

keyboard.diode_orientation = DiodeOrientation.COLUMNS


# ------------------User level config variables ---------------------------------------
keyboard.unicode_mode = UnicodeMode.LINUX
keyboard.tap_time = 350
keyboard.leader_timeout = 2000
keyboard.debug_enabled = False

emoticons = compile_unicode_string_sequences({
    # Emoticons, but fancier
    'ANGRY_TABLE_FLIP': r'(ノಠ痊ಠ)ノ彡┻━┻',
    'CHEER': r'+｡:.ﾟヽ(´∀｡)ﾉﾟ.:｡+ﾟﾟ+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟ',
    'TABLE_FLIP': r'(╯°□°）╯︵ ┻━┻',
    'WAT': r'⊙.☉',
    'FF': r'凸(ﾟДﾟ#)',
    'F': r'（￣^￣）凸',
    'MEH': r'╮(￣_￣)╭',
    'YAY': r'o(^▽^)o',
})

# ---------------------- Leader Key Macros --------------------------------------------

keyboard.leader_dictionary = {
    'flip': emoticons.ANGRY_TABLE_FLIP,
    'cheer': emoticons.CHEER,
    'wat': emoticons.WAT,
    'ff': emoticons.FF,
    'f': emoticons.F,
    'meh': emoticons.MEH,
    'yay': emoticons.YAY,
}

WPM = send_string("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Bibendum arcu vitae elementum curabitur vitae nunc sed. Facilisis sed odio morbi quis.")

# ---------------------- Keymap ---------------------------------------------------------

keyboard.keymap = [
    [
        KC.GESC,   KC.W,    KC.E,    KC.R,    KC.T,    KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,
        KC.A,    KC.S,    KC.D,    KC.F,    KC.G,    KC.H,    KC.J,    KC.K,    KC.L,    KC.ESC,
        KC.Z,    KC.X,    KC.C,    KC.V,    KC.BSPC, KC.SPC,  KC.B,    KC.N,    KC.M,    KC.ENT,
    ],
]

if __name__ == '__main__':
    keyboard.go()
