from kmk.modules.split import AbstractSplit
from kmk.transports.pio_uart import PIO_UART
from kmk.transports.uart_split import UartSplit


class PioSplit(UartSplit):
    '''Enables splitting wired keyboards using RP2040'''

    def during_bootup(self, keyboard):
        AbstractSplit.during_bootup(self, keyboard)

        # Fallback to default data pin in keyboard config
        if not self.data_pin:
            self.data_pin = keyboard.data_pin

        if self.data_pin is None:
            raise Exception('UART Split requires data_pin argument')

        # Init the protocol
        if self._is_target or not self.uart_flip:
            self._uart = PIO_UART(tx=self.data_pin2, rx=self.data_pin)
        else:
            self._uart = PIO_UART(tx=self.data_pin, rx=self.data_pin2)
