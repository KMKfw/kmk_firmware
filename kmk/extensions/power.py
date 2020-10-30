import board
import digitalio

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
from kmk.kmktime import sleep_ms, ticks_diff, ticks_ms


class Power(Extension):
    def __init__(self, powersave_pin=None, enable=False, is_target=True):
        self.enable = enable
        self.powersave_pin = powersave_pin  # Powersave pin board object
        self.is_target = is_target
        self._powersave_start = ticks_ms()
        self._usb_last_scan = ticks_ms() - 5000
        self._psp = None  # Powersave pin object
        self._i2c = None

        make_key(
            names=('PS_TOG',), on_press=self._ps_tog, on_release=handler_passthrough
        )
        make_key(
            names=('PS_ENB',), on_press=self._ps_enable, on_release=handler_passthrough
        )
        make_key(
            names=('PS_DIS',), on_press=self._ps_disable, on_release=handler_passthrough
        )

    def __repr__(self):
        return f'Power({self._to_dict()})'

    def _to_dict(self):
        return f'''Power(
        enable={self.enable}
        powersave_pin={self.powersave_pin}
        is_target={self.is_target}
        _powersave_start={self._powersave_start}
        _usb_last_scan={self._usb_last_scan}
        _psp={self._psp} )
        '''

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        self.disable_powersave

    def during_bootup(self, keyboard):
        self._detect_i2c()
        self.enable = not bool(self.usb_scan)

    def before_matrix_scan(self, keyboard):
        if self.usb_rescan_timer():
            self.enable = not bool(self.usb_scan)

    def after_matrix_scan(self, keyboard, matrix_update):
        if matrix_update:
            self.psave_time_reset()
        else:
            self.psleep()

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def enable_powersave(self):
        '''Enables power saving features'''
        print('Psave True')
        if self.powersave_pin:
            # Allows power save to prevent RGB drain.
            # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic

            if not self._psp:
                self._psp = digitalio.DigitalInOut(self.powersave_pin)
            self._psp.direction = digitalio.Direction.OUTPUT
            self._psp.value = True

        self.enable = True

    def disable_powersave(self):
        '''Disables power saving features'''
        print('Psave False')
        if self.powersave_pin:
            # Allows power save to prevent RGB drain.
            # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic

            if not self._psp:
                self._psp = digitalio.DigitalInOut(self.powersave_pin)
            self._psp.direction = digitalio.Direction.OUTPUT
            self._psp.value = False

        self.enable = False

    def psleep(self):
        '''
        Sleeps longer and longer to save power the more time in between updates.
        '''
        if ticks_diff(ticks_ms(), self._powersave_start) <= 20000 and self.is_target:
            sleep_ms(1)
        elif ticks_diff(ticks_ms(), self._powersave_start) <= 40000 and self.is_target:
            sleep_ms(4)
        elif ticks_diff(ticks_ms(), self._powersave_start) <= 60000 and self.is_target:
            sleep_ms(8)
        elif ticks_diff(ticks_ms(), self._powersave_start) >= 240000:
            sleep_ms(250)

    def psave_time_reset(self):
        self._powersave_start = ticks_ms()

    def usb_rescan_timer(self):
        return bool(ticks_diff(ticks_ms(), self._usb_last_scan) > 5000)

    def usb_time_reset(self):
        self._usb_last_scan = ticks_ms()

    def usb_scan(self):
        # TODO Add USB detection here. Currently lies that it's connected
        # https://github.com/adafruit/circuitpython/pull/3513
        return True

    def _detect_i2c(self):
        '''Detects i2c devices and disables cutting power to them'''
        # TODO Figure out how this could deinit/reinit instead.
        self._i2c = board.I2C()
        devices = self._i2c.scan()
        if devices != []:
            self.powersave_pin = None

    def _ps_tog(self):
        if self.enable:
            self.enable_powersave()
        else:
            self.disable_powersave()

    def _ps_enable(self):
        if not self.enable:
            self.enable_powersave()

    def _ps_disable(self):
        if self.enable:
            self.disable_powersave()
