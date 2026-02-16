import board

# Bit-C-Pro RP2040 pinout for reference, see https://nullbits.co/bit-c-pro/
# (unused)
pinout = [
    board.D0,
    board.D1,
    None,  # GND
    None,  # GND
    board.D2,
    board.D3,
    board.D4,  # breakout SDA
    board.D5,  # breakout SCL
    board.D6,
    board.D7,
    board.D8,
    board.D9,
    # Unconnected breakout pins D11, D12, GND, D13, D14
    board.D21,  # WS2812 LEDs labeled D10/GP21 but only board.D21 is defined
    board.D23,  # MOSI
    board.D20,  # MISO
    board.D22,  # SCK
    board.D26,
    board.D27,
    board.D28,
    board.D29,
    None,  # 3.3v
    None,  # RST
    None,  # GND
    None,  # RAW
]
# also defined: board.LED_RED, board.LED_GREEN, and board.LED_BLUE == board.LED
