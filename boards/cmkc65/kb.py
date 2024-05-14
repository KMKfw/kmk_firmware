import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    col_pins = (
        board.P1_00,
        board.P0_17,
        board.P0_22,
        board.P0_20,

    )
    row_pins = (
		board.P0_29,
		board.P0_02,
		board.P1_15,
		board.P1_13,
		board.P1_11,
    )
	
    SCL=board.P0_09
    SDA=board.P0_10
	
    diode_orientation = DiodeOrientation.COLUMNS