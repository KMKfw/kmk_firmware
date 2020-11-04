import board
import digitalio

from kmk.extensions import Extension
from kmk.handlers.stock import passthrough as handler_passthrough
from kmk.keys import make_key
from kmk.kmktime import sleep_ms, ticks_diff, ticks_ms


class Power(Extension):
    def __init__(self, powersave_pin=None):
        self.enable = False
        self.powersave_pin = powersave_pin  # Powersave pin board object
        self._powersave_start = ticks_ms()
        self._usb_last_scan = ticks_ms() - 5000
        self._psp = None  # Powersave pin object
        self._i2c = None
        self._loopcounter = 0

        make_key(
            names=('PS_TOG',), on_press=self._ps_tog, on_release=handler_passthrough
        )
        make_key(
            names=('PS_ON',), on_press=self._ps_enable, on_release=handler_passthrough
        )
        make_key(
            names=('PS_OFF',), on_press=self._ps_disable, on_release=handler_passthrough
        )

    def __repr__(self):
        return f'Power({self._to_dict()})'

    def _to_dict(self):
        return f'''Power(
        enable={self.enable}
        powersave_pin={self.powersave_pin}
        _powersave_start={self._powersave_start}
        _usb_last_scan={self._usb_last_scan}
        _psp={self._psp} )
        '''

    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        self.disable_powersave()

    def during_bootup(self, keyboard):
        self._i2c_scan()
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard, matrix_update):
        if matrix_update:
            self.psave_time_reset()
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        if self.enable:
            self.psleep()

    def on_powersave_enable(self, keyboard):
        '''Gives 10 cycles to allow other extentions to clean up before powersave'''
        if keyboard._trigger_powersave_enable:
            if self._loopcounter > 10:
                self._loopcounter += 1
                return
            self._loopcounter = 0
            keyboard._trigger_powersave_enable = False
            self.enable_powersave(keyboard)
        return

    def on_powersave_disable(self, keyboard):
        keyboard._trigger_powersave_disable = False
        self.disable_powersave()
        return

    def enable_powersave(self, keyboard):
        '''Enables power saving features'''
        print('Psave True')
        if keyboard.i2c_deinit_count >= self._i2c and self.powersave_pin:
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
        if ticks_diff(ticks_ms(), self._powersave_start) <= 60000:
            sleep_ms(8)
        elif ticks_diff(ticks_ms(), self._powersave_start) >= 240000:
            sleep_ms(180)

    def psave_time_reset(self):
        self._powersave_start = ticks_ms()

    def _i2c_scan(self):
        i2c = board.I2C()
        while not i2c.try_lock():
            pass
        try:
            self._i2c = len(i2c.scan())
        finally:
            i2c.unlock()

    def usb_rescan_timer(self):
        return bool(ticks_diff(ticks_ms(), self._usb_last_scan) > 5000)

    def usb_time_reset(self):
        self._usb_last_scan = ticks_ms()

    def usb_scan(self):
        # TODO Add USB detection here. Currently lies that it's connected
        # https://github.com/adafruit/circuitpython/pull/3513
        return True

    def _ps_tog(self, key, keyboard, *args, **kwargs):
        if self.enable:
            keyboard._trigger_powersave_disable = True
        else:
            keyboard._trigger_powersave_enable = True

    def _ps_enable(self, key, keyboard, *args, **kwargs):
        if not self.enable:
            keyboard._trigger_powersave_enable = True

    def _ps_disable(self, key, keyboard, *args, **kwargs):
        if self.enable:
            keyboard._trigger_powersave_disable = True
