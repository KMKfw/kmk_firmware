'''
Extension handles usage of Trackball Breakout by Pimoroni
Product page: https://shop.pimoroni.com/products/trackball-breakout
'''
from micropython import const

import math
import struct

from kmk.keys import make_key
from kmk.kmktime import PeriodicTimer
from kmk.modules import Module
from kmk.modules.mouse_keys import PointingDevice

I2C_ADDRESS = 0x0A
I2C_ADDRESS_ALTERNATIVE = 0x0B

CHIP_ID = 0xBA11
VERSION = 1

REG_LED_RED = 0x00
REG_LED_GRN = 0x01
REG_LED_BLU = 0x02
REG_LED_WHT = 0x03

REG_LEFT = 0x04
REG_RIGHT = 0x05
REG_UP = 0x06
REG_DOWN = 0x07
REG_SWITCH = 0x08
MSK_SWITCH_STATE = 0b10000000

REG_USER_FLASH = 0xD0
REG_FLASH_PAGE = 0xF0
REG_INT = 0xF9
MSK_INT_TRIGGERED = 0b00000001
MSK_INT_OUT_EN = 0b00000010
REG_CHIP_ID_L = 0xFA
RED_CHIP_ID_H = 0xFB
REG_VERSION = 0xFC
REG_I2C_ADDR = 0xFD
REG_CTRL = 0xFE
MSK_CTRL_SLEEP = 0b00000001
MSK_CTRL_RESET = 0b00000010
MSK_CTRL_FREAD = 0b00000100
MSK_CTRL_FWRITE = 0b00001000

ANGLE_OFFSET = 0


class TrackballMode:
    '''Behaviour mode of trackball: mouse movement or vertical scroll'''

    MOUSE_MODE = const(0)
    SCROLL_MODE = const(1)


class TrackballLayer:
    '''Just to show an interface for layers'''

    def handle(self, keyboard, trackball, x, y, switch, state):
        raise NotImplementedError


class PointingLayer(TrackballLayer):
    '''the default behavior: act as trackball'''

    def handle(self, keyboard, trackball, x, y, switch, state):
        if trackball.mode == TrackballMode.MOUSE_MODE:
            if x >= 0:
                trackball.pointing_device.report_x[0] = x
            else:
                trackball.pointing_device.report_x[0] = 0xFF & x
            if y >= 0:
                trackball.pointing_device.report_y[0] = y
            else:
                trackball.pointing_device.report_y[0] = 0xFF & y
            trackball.pointing_device.hid_pending = x != 0 or y != 0
        else:  # SCROLL_MODE
            trackball.pointing_device.report_w[0] = y
            trackball.pointing_device.hid_pending = y != 0

        if switch == 1:  # Button pressed
            trackball.pointing_device.button_status[
                0
            ] |= trackball.pointing_device.MB_LMB
            trackball.pointing_device.hid_pending = True

        if not state and trackball.previous_state is True:  # Button released
            trackball.pointing_device.button_status[
                0
            ] &= ~trackball.pointing_device.MB_LMB
            trackball.pointing_device.hid_pending = True

        trackball.previous_state = state


class KeyLayer(TrackballLayer):
    '''Act like an encoder.'''

    x = 0
    y = 0

    def __init__(self, up, right, down, left, press, axis_snap=0.25, steps=8):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.press = press
        '''snap to axis. the higher the value, the more we snap to the dominant direction'''
        self.axis_snap = axis_snap
        '''how many px we move to trigger a key tap, less means more key taps'''
        self.steps = steps

    def handle(self, keyboard, trackball, x, y, switch, state):
        if y and abs(x / y) < self.axis_snap:
            x = 0
        if x and abs(y / x) < self.axis_snap:
            y = 0

        self.x += x
        self.y += y
        x_taps = self.x // self.steps
        y_taps = self.y // self.steps
        self.x %= self.steps
        self.y %= self.steps
        for i in range(x_taps, 0, 1):
            keyboard.tap_key(self.left)
        for i in range(x_taps, 0, -1):
            keyboard.tap_key(self.right)
        for i in range(y_taps, 0, 1):
            keyboard.tap_key(self.up)
        for i in range(y_taps, 0, -1):
            keyboard.tap_key(self.down)
        if switch and state:
            keyboard.tap_key(self.press)


class Trackball(Module):
    '''Module handles usage of Trackball Breakout by Pimoroni'''

    def __init__(
        self,
        i2c,
        mode=TrackballMode.MOUSE_MODE,
        address=I2C_ADDRESS,
        angle_offset=ANGLE_OFFSET,
        layers=None,
    ):
        self.angle_offset = angle_offset
        if layers is None:
            layers = [PointingLayer()]
        self._i2c_address = address
        self._i2c_bus = i2c

        self.pointing_device = PointingDevice()
        self.mode = mode
        self.previous_state = False  # click state
        self.layers = layers
        self.polling_interval = 20

        chip_id = struct.unpack('<H', bytearray(self._i2c_rdwr([REG_CHIP_ID_L], 2)))[0]
        if chip_id != CHIP_ID:
            raise RuntimeError(
                'Invalid chip ID: 0x{:04X}, expected 0x{:04X}'.format(chip_id, CHIP_ID)
            )

        make_key(
            names=('TB_MODE',),
            on_press=self._tb_mode_press,
            on_release=self._tb_mode_press,
        )

    def during_bootup(self, keyboard):
        self._timer = PeriodicTimer(self.polling_interval)

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        if not self._timer.tick():
            return

        up, down, left, right, switch, state = self._read_raw_state()

        x, y = self._calculate_movement(right - left, down - up)

        layer = self.layers[-1]
        active_layer = keyboard.active_layers[0]
        if len(self.layers) > active_layer:
            layer = self.layers[active_layer]
        layer.handle(keyboard, self, x, y, switch, state)

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

    def set_rgbw(self, r, g, b, w):
        '''Set all LED brightness as RGBW.'''
        self._i2c_rdwr([REG_LED_RED, r, g, b, w])

    def set_red(self, value):
        '''Set brightness of trackball red LED.'''
        self._i2c_rdwr([REG_LED_RED, value & 0xFF])

    def set_green(self, value):
        '''Set brightness of trackball green LED.'''
        self._i2c_rdwr([REG_LED_GRN, value & 0xFF])

    def set_blue(self, value):
        '''Set brightness of trackball blue LED.'''
        self._i2c_rdwr([REG_LED_BLU, value & 0xFF])

    def set_white(self, value):
        '''Set brightness of trackball white LED.'''
        self._i2c_rdwr([REG_LED_WHT, value & 0xFF])

    def _clear_pending_hid(self):
        self.pointing_device.hid_pending = False
        self.pointing_device.report_x[0] = 0
        self.pointing_device.report_y[0] = 0
        self.pointing_device.report_w[0] = 0
        self.pointing_device.button_status[0] = 0

    def _read_raw_state(self):
        '''Read up, down, left, right and switch data from trackball.'''
        left, right, up, down, switch = self._i2c_rdwr([REG_LEFT], 5)
        switch, switch_state = (
            switch & ~MSK_SWITCH_STATE,
            (switch & MSK_SWITCH_STATE) > 0,
        )
        return up, down, left, right, switch, switch_state

    def _i2c_rdwr(self, data, length=0):
        '''Write and optionally read I2C data.'''
        while not self._i2c_bus.try_lock():
            pass

        try:
            if length > 0:
                result = bytearray(length)
                self._i2c_bus.writeto_then_readfrom(
                    self._i2c_address, bytes(data), result
                )
                return list(result)
            else:
                self._i2c_bus.writeto(self._i2c_address, bytes(data))

            return []

        finally:
            self._i2c_bus.unlock()

    def _tb_mode_press(self, key, keyboard, *args, **kwargs):
        self.mode = not self.mode

    def _calculate_movement(self, raw_x, raw_y):
        '''Calculate accelerated movement vector from raw data'''
        if raw_x == 0 and raw_y == 0:
            return 0, 0

        var_accel = 1
        power = 2.5

        angle_rad = math.atan2(raw_y, raw_x) + self.angle_offset
        vector_length = math.sqrt(pow(raw_x, 2) + pow(raw_y, 2))
        vector_length = pow(vector_length * var_accel, power)
        x = math.floor(vector_length * math.cos(angle_rad))
        y = math.floor(vector_length * math.sin(angle_rad))

        limit = 127  # hid size limit
        x_clamped = max(min(limit, x), -limit)
        y_clamped = max(min(limit, y), -limit)

        return x_clamped, y_clamped
