'''
Extension handles usage of Trackball Breakout by Pimoroni
Product page: https://shop.pimoroni.com/products/trackball-breakout
'''
from micropython import const

import math
import struct
from adafruit_pixelbuf import PixelBuf

from kmk.keys import AX, KC, make_argumented_key, make_key
from kmk.kmktime import PeriodicTimer
from kmk.modules import Module
from kmk.utils import Debug

_I2C_ADDRESS = const(0x0A)
_I2C_ADDRESS_ALTERNATIVE = const(0x0B)

_CHIP_ID = const(0xBA11)
_VERSION = const(1)

_REG_LED_RED = const(0x00)
_REG_LED_GRN = const(0x01)
_REG_LED_BLU = const(0x02)
_REG_LED_WHT = const(0x03)

_REG_LEFT = const(0x04)
_REG_RIGHT = const(0x05)
_REG_UP = const(0x06)
_REG_DOWN = const(0x07)
_REG_SWITCH = const(0x08)
_MSK_SWITCH_STATE = const(0b10000000)

_REG_USER_FLASH = const(0xD0)
_REG_FLASH_PAGE = const(0xF0)
_REG_INT = const(0xF9)
_MSK_INT_TRIGGERED = const(0b00000001)
_MSK_INT_OUT_EN = const(0b00000010)
_REG_CHIP_ID_L = const(0xFA)
_REG_CHIP_ID_H = const(0xFB)
_REG_VERSION = const(0xFC)
_REG_I2C_ADDR = const(0xFD)
_REG_CTRL = const(0xFE)
_MSK_CTRL_SLEEP = const(0b00000001)
_MSK_CTRL_RESET = const(0b00000010)
_MSK_CTRL_FREAD = const(0b00000100)
_MSK_CTRL_FWRITE = const(0b00001000)


debug = Debug(__name__)


class TrackballHandlerKeyMeta:
    def __init__(self, handler=0):
        self.handler = handler


def layer_key_validator(handler):
    return TrackballHandlerKeyMeta(handler=handler)


class TrackballMode:
    '''Behaviour mode of trackball: mouse movement or vertical scroll'''

    MOUSE_MODE = const(0)
    SCROLL_MODE = const(1)


class ScrollDirection:
    '''Behaviour mode of scrolling: natural or reverse scrolling'''

    NATURAL = const(0)
    REVERSE = const(1)


class TrackballHandler:
    def handle(self, keyboard, trackball, x, y, switch, state):
        raise NotImplementedError


class PointingHandler(TrackballHandler):
    def handle(self, keyboard, trackball, x, y, switch, state):
        if x:
            AX.X.move(keyboard, x)
        if y:
            AX.Y.move(keyboard, y)

        if switch == 1:  # Button changed state
            keyboard.pre_process_key(KC.MB_LMB, is_pressed=state)


class ScrollHandler(TrackballHandler):
    def __init__(self, scroll_direction=ScrollDirection.NATURAL):
        self.scroll_direction = scroll_direction

    def handle(self, keyboard, trackball, x, y, switch, state):
        if self.scroll_direction == ScrollDirection.REVERSE:
            y = -y

        if y != 0:
            AX.W.move(keyboard, y)

        if switch == 1:  # Button changed state
            keyboard.pre_process_key(KC.MB_LMB, is_pressed=state)


class KeyHandler(TrackballHandler):
    x = 0
    y = 0

    def __init__(self, up, right, down, left, press, axis_snap=0.25, steps=8):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.press = press
        self.axis_snap = axis_snap
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
        address=_I2C_ADDRESS,
        angle_offset=0,
        handlers=None,
    ):
        self.angle_offset = angle_offset
        if not handlers:
            handlers = [PointingHandler(), ScrollHandler()]
            if mode == TrackballMode.SCROLL_MODE:
                handlers.reverse()
        self._i2c_address = address
        self._i2c_bus = i2c

        self.mode = mode
        self.handlers = handlers
        self.current_handler = self.handlers[0]
        self.polling_interval = 20

        make_key(
            names=('TB_MODE', 'TB_NEXT_HANDLER', 'TB_N'),
            on_press=self._tb_handler_next_press,
        )

        make_argumented_key(
            validator=layer_key_validator,
            names=('TB_HANDLER', 'TB_H'),
            on_press=self._tb_handler_press,
        )

    def during_bootup(self, keyboard):
        chip_id = struct.unpack('<H', bytearray(self._i2c_rdwr([_REG_CHIP_ID_L], 2)))[0]
        if chip_id != _CHIP_ID:
            raise RuntimeError(
                f'Invalid chip ID: 0x{chip_id:04X}, expected 0x{_CHIP_ID:04X}'
            )

        self._timer = PeriodicTimer(self.polling_interval)

        a = math.pi * self.angle_offset / 180
        self.rot = [[math.cos(a), math.sin(a)], [-math.sin(a), math.cos(a)]]

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        if not self._timer.tick():
            return

        if not (self._i2c_rdwr([_REG_INT], 1)[0] & _MSK_INT_TRIGGERED):
            return

        up, down, left, right, switch, state = self._read_raw_state()

        x, y = self._calculate_movement(right - left, down - up)

        self.current_handler.handle(keyboard, self, x, y, switch, state)

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def set_rgbw(self, r, g, b, w):
        '''Set all LED brightness as RGBW.'''
        self._i2c_rdwr([_REG_LED_RED, r, g, b, w])

    def set_red(self, value):
        '''Set brightness of trackball red LED.'''
        self._i2c_rdwr([_REG_LED_RED, value & 0xFF])

    def set_green(self, value):
        '''Set brightness of trackball green LED.'''
        self._i2c_rdwr([_REG_LED_GRN, value & 0xFF])

    def set_blue(self, value):
        '''Set brightness of trackball blue LED.'''
        self._i2c_rdwr([_REG_LED_BLU, value & 0xFF])

    def set_white(self, value):
        '''Set brightness of trackball white LED.'''
        self._i2c_rdwr([_REG_LED_WHT, value & 0xFF])

    def activate_handler(self, handler):
        if isinstance(handler, TrackballHandler):
            self.current_handler = handler
        else:
            try:
                self.current_handler = self.handlers[handler]
            except KeyError:
                if debug.enabled:
                    debug(f'no handler found with id {handler}')

    def next_handler(self):
        next_index = self.handlers.index(self.current_handler) + 1
        if next_index >= len(self.handlers):
            next_index = 0
        self.activate_handler(next_index)

    def _read_raw_state(self):
        '''Read up, down, left, right and switch data from trackball.'''
        left, right, up, down, switch = self._i2c_rdwr([_REG_LEFT], 5)
        switch_changed, switch_state = (
            switch & ~_MSK_SWITCH_STATE,
            (switch & _MSK_SWITCH_STATE) > 0,
        )
        return up, down, left, right, switch_changed, switch_state

    def _i2c_rdwr(self, data, length=0):
        '''Write and optionally read I2C data.'''
        if not self._i2c_bus.try_lock():
            return

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

    def _tb_handler_press(self, key, keyboard, *args, **kwargs):
        self.activate_handler(key.meta.handler)

    def _tb_handler_next_press(self, key, keyboard, *args, **kwargs):
        self.next_handler()

    def _calculate_movement(self, raw_x, raw_y):
        '''Calculate accelerated movement vector from raw data'''
        if raw_x == 0 and raw_y == 0:
            return 0, 0

        scale = math.sqrt(raw_x**2 + raw_y**2)
        x = (self.rot[0][0] * raw_x + self.rot[0][1] * raw_y) * scale
        y = (self.rot[1][0] * raw_x + self.rot[1][1] * raw_y) * scale

        return int(x), int(y)


class TrackballPixel(PixelBuf):
    '''PixelBuf interface for the Trackball RGBW LED'''

    def __init__(self, trackball, **kwargs):
        self.trackball = trackball
        kwargs['byteorder'] = 'RGBW'
        super().__init__(1, **kwargs)

    def deinit(self):
        super().deinit()
        self.trackball.set_rgbw(0, 0, 0, 0)

    def _transmit(self, b):
        self.trackball.set_rgbw(b[0], b[1], b[2], b[3])
