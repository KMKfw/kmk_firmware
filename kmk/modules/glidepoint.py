try:
    from typing import Callable
except ImportError:
    pass

from micropython import const

from kmk.keys import AX
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)

_ADDRESS = const(0x2A)

_MASK_READ = const(0xA0)
_MASK_WRITE = const(0x80)

_REG_FW_ID = const(0x00)
_REG_FW_VER = const(0x01)
_REG_STATUS = const(0x02)
_REG_SYS_CFG = const(0x03)
_REG_FEED_CFG1 = const(0x04)
_REG_FEED_CFG2 = const(0x05)
_REG_CAL_CFG = const(0x07)
_REG_AUX_CTL = const(0x08)
_REG_SAMPLE_RATE = const(0x09)
_REG_ZIDLE = const(0x0A)
_REG_Z_SCALER = const(0x0B)
_REG_SLEEP_INTERVAL = const(0x0C)
_REG_SLEEP_TIMER = const(0x0D)
_REG_DATA = const(0x12)

_FEED1_ENABLE = const(0x01)
_FEED1_ABSOLUTE = const(0x02)
_FEED1_NO_FILTER = const(0x04)
_FEED1_NO_X_DATA = const(0x08)
_FEED1_NO_Y_DATA = const(0x10)
_FEED1_INVERT_X = const(0x40)
_FEED1_INVERT_Y = const(0x80)

_FEED2_INTELLIMOUSE = const(0x01)
_FEED2_NO_TAPS = const(0x02)
_FEED2_NO_SEC_TAPS = const(0x04)
_FEED2_NO_SCROLL = const(0x08)
_FEED2_NO_GLIDEEXTEND = const(0x10)
_FEED2_SWAP_XY = const(0x80)


def with_i2c_lock(rw: Callable[[object, int], None]) -> Callable[[object, int], None]:
    def _(self, n: int) -> None:
        if not self._i2c.try_lock():
            if debug.enabled:
                debug("can't acquire lock")
            return
        try:
            rw(self, n)
        finally:
            self._i2c.unlock()

    return _


class AbsoluteHandler:
    cfg = (
        _REG_FEED_CFG2,
        0x00,
        _REG_FEED_CFG1,
        _FEED1_ENABLE | _FEED1_NO_FILTER | _FEED1_ABSOLUTE | _FEED1_INVERT_X,
    )

    def handle(buffer: bytearray, keyboard) -> None:
        button = buffer[0]
        x_low = buffer[2]
        y_low = buffer[3]
        high = buffer[4]
        z_lvl = buffer[5]

        x_pos = ((high & 0x0F) << 8) | x_low
        y_pos = ((high & 0xF0) << 4) | y_low

        if debug.enabled:
            debug(
                'buttons:',
                bin(button),
                ' x_pos:',
                x_pos,
                ' y_pos:',
                y_pos,
                'z_lvl:',
                z_lvl,
            )


class RelativeHandler:
    cfg = (
        _REG_FEED_CFG2,
        0x00,
        _REG_FEED_CFG1,
        _FEED1_ENABLE | _FEED1_NO_FILTER | _FEED1_INVERT_X,
    )

    def handle(buffer: bytearray, keyboard) -> None:
        button = buffer[0] & 0b00000111
        x_sign = buffer[0] & 0b00010000
        y_sign = buffer[0] & 0b00100000
        x_delta = buffer[1]
        y_delta = buffer[2]
        w_delta = buffer[3]

        if x_sign:
            x_delta -= 0xFF
        if y_sign:
            y_delta -= 0xFF

        if x_delta != 0:
            AX.X.move(keyboard, x_delta)
        if y_delta != 0:
            AX.Y.move(keyboard, y_delta)

        if debug.enabled:
            debug(
                'buttons:',
                bin(button),
                ' x_delta:',
                x_delta,
                ' y_delta:',
                y_delta,
                ' w_delta',
                w_delta,
            )


class GlidePoint(Module):
    def __init__(self, i2c):
        self._i2c = i2c
        self._buffer = bytearray(8)

        # self.handler = RelativeHandler
        self.handler = AbsoluteHandler

    @with_i2c_lock
    def _read(self, n: int) -> None:
        self._buffer[0] |= _MASK_READ
        self._i2c.writeto_then_readfrom(
            _ADDRESS, self._buffer, self._buffer, out_end=1, in_end=n
        )

    @with_i2c_lock
    def _write(self, n: int) -> None:
        for i in range(0, n, 2):
            self._buffer[i] |= _MASK_WRITE
        self._i2c.writeto(_ADDRESS, self._buffer, end=n)

    def _check_firmware(self) -> bool:
        self._buffer[0] = _REG_FW_ID
        self._read(2)
        return self._buffer[:2] == b'\x07:'

    def _clear_status_flags(self) -> None:
        self._buffer[0] = _REG_STATUS
        self._buffer[1] = 0x00
        self._write(2)

    def _configure(self) -> None:
        self._buffer[0] = _REG_SYS_CFG
        self._buffer[1] = 0x00
        for idx, val in enumerate(self.handler.cfg):
            self._buffer[idx + 2] = val
        self._write(2 + len(self.handler.cfg))

    def _data_ready(self) -> bool:
        self._buffer[0] = _REG_STATUS
        self._read(1)
        return self._buffer[0] != 0x00

    def during_bootup(self, keyboard):
        if not self._check_firmware:
            raise OSError('Firmware ID mismatch')

        self._clear_status_flags()
        self._configure()

    def before_matrix_scan(self, keyboard):
        pass

    def after_matrix_scan(self, keyboard):
        if not self._data_ready():
            return

        self._buffer[0] = _REG_DATA
        self._read(6)

        self.handler.handle(self._buffer, keyboard)

        self._clear_status_flags()

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        self._buffer[0] = _REG_SYS_CFG
        self._buffer[1] = 0x04
        self._write(2)

    def on_powersave_disable(self, keyboard):
        self._buffer[0] = _REG_SYS_CFG
        self._buffer[1] = 0x00
        self._write(2)
