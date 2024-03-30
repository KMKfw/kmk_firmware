import board

pinout = [
    # Left, top->bottom
    board.TX,
    board.RX,
    None,  # GND
    None,  # GND
    board.SDA,
    board.SCL,
    board.D4,
    board.D5,  # C6
    board.D6,  # D7
    board.D7,  # E6
    board.D8,  # B4
    board.D9,  # B5
    # Right, bottom->top
    board.D21,  # B6
    board.D23,  # B2
    board.D20,  # B3
    board.D22,  # B1
    board.D26,  # F7
    board.D27,  # F6
    board.D28,  # F5
    board.D29,  # F4
    None,  # 3.3v
    None,  # RST
    None,  # GND
    None,  # RAW
    # Bottom, left->right
    board.D12,
    board.D13,
    board.D14,
    board.D15,
    board.D16,
    # Internal
    board.NEOPIXEL,
    board.VBUS_SENSE,
    board.POWER_LED,
    board.I2C,
    board.SPI,
    board.UART,
]
