from kmk.extensions import Extension
from kmk.kmktime import sleep_ms, ticks_diff, ticks_ms


class Power(Extension):
    def __init__(self, powersave_pin=None, enable=False, is_target=True):
        self.enable = enable
        self.powersave_pin = powersave_pin
        self.is_target = is_target
        self._powersave_start = ticks_ms()
        self._usb_last_scan = ticks_ms() - 5000
        self._psp = None

    def __repr__(self):
        return f'Power({self._to_dict()})'

    def _to_dict(self):
        return f'Power( enable={self.enable} powersave_pin={self.powersave_pin} is_target={self.is_target} _powersave_start={self._powersave_start} _usb_last_scan={self._usb_last_scan} _psp={self._psp} )'

    def during_bootup(self, keyboard):
        self.enable = not bool(self.usb_scan)

    def before_matrix_scan(self, keyboard_state):
        if self.usb_rescan_timer():
            self.enable = not bool(self.usb_scan)

    def after_matrix_scan(self, keyboard_state, matrix_update):
        if matrix_update:
            self.psave_time_reset()
        else:
            self.psleep()

    def enable_powersave(self):
        print('Psave True')
        if self.powersave_pin:
            import digitalio

            # Allows power save to prevent RGB drain.
            # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic
            if not self._psp:
                self._psp = digitalio.DigitalInOut(self.powersave_pin)
            self._psp.direction = digitalio.Direction.OUTPUT
            self._psp.value = True
            # TODO Allow a hook to stop RGB/OLED to deinit or this causes a lockup

        self.enable = True

        return self

    def disable_powersave(self):
        print('Psave False')
        if self.powersave_pin:
            import digitalio

            # Allows power save to prevent RGB drain.
            # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic
            if not self._psp:
                self._psp = digitalio.DigitalInOut(self.powersave_pin)
            self._psp.direction = digitalio.Direction.OUTPUT
            self._psp.value = False
            # TODO Allow a hook to stop RGB/OLED to reinit

        self.enable = False

        return self

    def psleep(self):
        '''
        Sleeps longer and longer to save power the more time in between updates.
        '''
        if ticks_diff(ticks_ms(), self.powersave_start) <= 20000 and self.is_target:
            sleep_ms(1)
        elif ticks_diff(ticks_ms(), self.powersave_start) <= 40000 and self.is_target:
            sleep_ms(4)
        elif ticks_diff(ticks_ms(), self.powersave_start) <= 60000 and self.is_target:
            sleep_ms(8)
        elif ticks_diff(ticks_ms(), self.powersave_start) >= 240000:
            sleep_ms(250)

    def psave_time_reset(self):
        self.powersave_start = ticks_ms()
        return self

    def usb_rescan_timer(self):
        return bool(ticks_diff(ticks_ms(), self.usb_last_scan) > 5000)

    def usb_time_reset(self):
        self.usb_last_scan = ticks_ms()
        return self

    def usb_scan(self):
        # TODO Add USB detection here. Currently lies that it's connected
        return True
