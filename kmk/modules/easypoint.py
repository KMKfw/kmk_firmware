'''
Extension handles usage of AS5013 by AMS
'''

from supervisor import ticks_ms

from kmk.modules import Module
from kmk.modules.mouse_keys import PointingDevice

I2C_ADDRESS = 0x40
I2X_ALT_ADDRESS = 0x41

X = 0x10
Y_RES_INT = 0x11

XP = 0x12
XN = 0x13
YP = 0x14
YN = 0x15

M_CTRL = 0x2B
T_CTRL = 0x2D

Y_OFFSET = 17
X_OFFSET = 7

DEAD_X = 5
DEAD_Y = 5


class Easypoint(Module):
    '''Module handles usage of AS5013 by AMS'''

    def __init__(
        self,
        i2c,
        address=I2C_ADDRESS,
        y_offset=Y_OFFSET,
        x_offset=X_OFFSET,
        dead_x=DEAD_X,
        dead_y=DEAD_Y,
    ):
        self._i2c_address = address
        self._i2c_bus = i2c

        # HID parameters
        self.pointing_device = PointingDevice()
        self.polling_interval = 20
        self.last_tick = ticks_ms()

        # Offsets for poor soldering
        self.y_offset = y_offset
        self.x_offset = x_offset

        # Deadzone
        self.dead_x = DEAD_X
        self.dead_y = DEAD_Y

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        now = ticks_ms()
        if now - self.last_tick < self.polling_interval:
            return
        self.last_tick = now

        x, y = self._read_raw_state()

        # I'm a shit coder, so offset is handled in software side
        s_x = self.getSignedNumber(x, 8) - self.x_offset
        s_y = self.getSignedNumber(y, 8) - self.y_offset

        # Evaluate Deadzone
        if s_x in range(-self.dead_x, self.dead_x) and s_y in range(
            -self.dead_y, self.dead_y
        ):
            # Within bounds, just die
            return
        else:
            # Set the X/Y from easypoint
            self.pointing_device.report_x[0] = x
            self.pointing_device.report_y[0] = y

            self.pointing_device.hid_pending = x != 0 or y != 0

        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        if self.pointing_device.hid_pending:
            keyboard._hid_helper.hid_send(self.pointing_device._evt)
            self._clear_pending_hid()
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def _clear_pending_hid(self):
        self.pointing_device.hid_pending = False
        self.pointing_device.report_x[0] = 0
        self.pointing_device.report_y[0] = 0
        self.pointing_device.report_w[0] = 0
        self.pointing_device.button_status[0] = 0

    def _read_raw_state(self):
        '''Read data from AS5013'''
        x, y = self._i2c_rdwr([X], length=2)
        return x, y

    def getSignedNumber(self, number, bitLength=8):
        mask = (2 ** bitLength) - 1
        if number & (1 << (bitLength - 1)):
            return number | ~mask
        else:
            return number & mask

    def _i2c_rdwr(self, data, length=1):
        '''Write and optionally read I2C data.'''
        while not self._i2c_bus.try_lock():
            pass

        try:
            if length > 0:
                result = bytearray(length)
                self._i2c_bus.writeto_then_readfrom(
                    self._i2c_address, bytes(data), result
                )
                return result
            else:
                self._i2c_bus.writeto(self._i2c_address, bytes(data))
            return []
        finally:
            self._i2c_bus.unlock()
