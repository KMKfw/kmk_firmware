'''
Circuit Python wrapper around PIO implementation of UART
Original source of these examples: https://github.com/adafruit/Adafruit_CircuitPython_PIOASM/tree/main/examples (MIT)
'''
import rp2pio
from array import array

'''
.program uart_tx
.side_set 1 opt
; An 8n1 UART transmit program.
; OUT pin 0 and side-set pin 0 are both mapped to UART TX pin.
  pull side 1 [7] ; Assert stop bit, or stall with line in idle state
  set x, 7 side 0 [7] ; Preload bit counter, assert start bit for 8 clocks
bitloop: ; This loop will run 8 times (8n1 UART)
  out pins, 1 ; Shift 1 bit from OSR to the first OUT pin
  jmp x-- bitloop [6] ; Each loop iteration is 8 cycles.

; compiles to:
'''
tx_code = array('H', [40864, 63271, 24577, 1602])


'''
.program uart_rx_mini

; Minimum viable 8n1 UART receiver. Wait for the start bit, then sample 8 bits
; with the correct timing.
; IN pin 0 is mapped to the GPIO used as UART RX.
; Autopush must be enabled, with a threshold of 8.

    wait 0 pin 0        ; Wait for start bit
    set x, 7 [10]       ; Preload bit counter, delay until eye of first data bit
bitloop:                ; Loop 8 times
    in pins, 1          ; Sample data
    jmp x-- bitloop [6] ; Each iteration is 8 cycles

; compiles to:
'''
rx_code = array('H', [8224, 59943, 16385, 1602])


class PIO_UART:
    def __init__(self, *, tx, rx, baudrate=9600):
        if tx:
            self.tx_pio = rp2pio.StateMachine(
                tx_code,
                first_out_pin=tx,
                first_sideset_pin=tx,
                frequency=8 * baudrate,
                initial_sideset_pin_state=1,
                initial_sideset_pin_direction=1,
                initial_out_pin_state=1,
                initial_out_pin_direction=1,
                sideset_enable=True,
            )
        if rx:
            self.rx_pio = rp2pio.StateMachine(
                rx_code,
                first_in_pin=rx,
                frequency=8 * baudrate,
                auto_push=True,
                push_threshold=8,
            )

    @property
    def timeout(self):
        return 0

    @property
    def baudrate(self):
        return self.tx_pio.frequency // 8

    @baudrate.setter
    def baudrate(self, frequency):
        self.tx_pio.frequency = frequency * 8
        self.rx_pio.frequency = frequency * 8

    def write(self, buf):
        return self.tx_pio.write(buf)

    @property
    def in_waiting(self):
        return self.rx_pio.in_waiting

    def read(self, n):
        b = bytearray(n)
        n = self.rx_pio.readinto(b)
        return b[:n]

    def readinto(self, buf):
        return self.rx_pio.readinto(buf)
