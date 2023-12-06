import board

# Bit-C-Pro RP2040 pinout for reference, see https://nullbits.co/bit-c-pro/
# (unused)
pinout = [
    board.D0,  # Enc 3
    board.D1,  # Enc 3
    None,  # GND
    None,  # GND
    board.D2,  # Enc 2
    board.D3,  # Enc 2
    board.D4,  # Row 4 + breakout SDA
    board.D5,  # Row 3 + breakout SCL
    board.D6,  # Row 2
    board.D7,  # Row 1
    board.D8,  # Enc 1
    board.D9,  # Enc 1
    # Unconnected breakout pins D11, D12, GND, D13, D14
    board.D21,  # WS2812 LEDs labeled D10/GP21 but only board.D21 is defined
    board.D23,  # MOSI - Enc 0
    board.D20,  # MISO - Enc 0
    board.D22,  # SCK - Row 0
    board.D26,  # A0 - Col 3
    board.D27,  # A1 - Col 2
    board.D28,  # A2 - Col 1
    board.D29,  # A3 - Col 0
    None,  # 3.3v
    None,  # RST
    None,  # GND
    None,  # RAW
]
# also defined: board.LED_RED, board.LED_GREEN, and board.LED_BLUE == board.LED
