from kmk.kmktime import sleep_ms, ticks_diff, ticks_ms


class power:
    def __init__(self, powersave_pin=None, enable=False):
        self.enable = enable
        self.powersave_pin = powersave_pin
        self.powersave_start = ticks_ms()
        self.ble_last_scan = ticks_ms() - 5000
        self.usb_last_scan = ticks_ms() - 5000
        self._psp = None

    def enable_powersave(self, board_name):
        print('Enabling power save')
        if self.powersave_pin:
            import digitalio

            if board_name == 'nice_nano':
                # Allows power save to prevent RGB drain.
                # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic
                if not self._psp:
                    self._psp = digitalio.DigitalInOut(self.powersave_pin)
                self._psp.direction = digitalio.Direction.OUTPUT
                self._psp.value = True

        self.enable = True

        return self

    def disable_powersave(self, board=None):
        print('Disabling power save')
        if self.powersave_pin:
            import digitalio

            if board == 'nice_nano':
                # Allows power save to prevent RGB drain.
                # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic
                if not self._psp:
                    self._psp = digitalio.DigitalInOut(self.powersave_pin)
                self._psp.direction = digitalio.Direction.OUTPUT
                self._psp.value = False

        self.enable = False

        return self

    def psleep(self, is_target):
        '''
        Sleeps longer and longer to save power the more time in between updates.
        '''
        if ticks_diff(ticks_ms(), self.powersave_start) <= 20000 and is_target:
            sleep_ms(1)
        elif ticks_diff(ticks_ms(), self.powersave_start) <= 40000 and is_target:
            sleep_ms(4)
        elif ticks_diff(ticks_ms(), self.powersave_start) <= 60000 and is_target:
            sleep_ms(8)
        elif ticks_diff(ticks_ms(), self.powersave_start) >= 240000:
            sleep_ms(250)

    def psave_time_reset(self):
        self.powersave_start = ticks_ms()
        return self

    def ble_rescan_timer(self):
        return bool(ticks_diff(ticks_ms(), self.ble_last_scan) > 5000)

    def ble_time_reset(self):
        self.ble_last_scan = ticks_ms()
        return self

    def usb_rescan_timer(self):
        return bool(ticks_diff(ticks_ms(), self.usb_last_scan) > 5000)

    def usb_time_reset(self):
        self.usb_last_scan = ticks_ms()
        return self
