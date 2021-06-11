import board


from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
from kmk.matrix import intify_coordinate as ic


class KMKKeyboard(_KMKKeyboard):
    col_pins = (board.D6, board.D7, board.D8, board.D9, board.D10, board.D11, board.D12)
    row_pins = (board.D1, board.D2, board.D3, board.D4, board.D5)

    # diode_orientation = DiodeOrientation.ROWS
    diode_orientation = DiodeOrientation.COLUMNS

    split_type = "UART"  # TODO add bluetooth support as well
    split_flip = True
    split_offsets = [5, 5, 5, 5, 5, 5, 5]
    # uart_pin = board.P0_08
    # rgb_pixel_pin = board.P0_06
    # extra_data_pin = board.SDA  # TODO This is incorrect. Find better solution
