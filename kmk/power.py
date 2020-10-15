from kmk.kmktime import sleep_ms, ticks_diff, ticks_ms

class power:
    def __init__(self, powersave_pin=None, enable=False):
        self.enable = enable
        self.powersave_pin = powersave_pin
        self.powersave_start = ticks_ms()
        self.ble_last_scan = ticks_ms() - 5000


    def enable_powersave(self):
        if self.powersave_pin:
            import digitalio
            # Allows power save to prevent RGB drain.
            # Example here https://docs.nicekeyboards.com/#/nice!nano/pinout_schematic
            psp = digitalio.DigitalInOut(self.powersave_pin)
            psp.direction = digitalio.Direction.OUTPUT
            psp.value = True

        self.enable = True

        return self

    def psleep(self, is_target):
        '''
        Sleeps longer and longer to save power the more time in between updates.
        '''
        if (
            ticks_diff(ticks_ms(), self.powersave_start) <= 20000 and is_target
        ):
            sleep_ms(1)
        elif (
            ticks_diff(ticks_ms(), self.powersave_start) <= 40000 and is_target
        ):
            sleep_ms(4)
        elif (
            ticks_diff(ticks_ms(), self.powersave_start) <= 60000 and is_target
        ):
            sleep_ms(8)
        elif ticks_diff(ticks_ms(), self.powersave_start) >= 240000:
            sleep_ms(250)


    def psave_time_reset(self):
        self.powersave_start = ticks_ms()
        return self

    def ble_rescan_timer(self):
        if ticks_diff(ticks_ms(), self.ble_last_scan) > 5000:
            return True
        else:
            return False

    def ble_time_reset(self):
        self.ble_last_scan = ticks_ms()
        return self
