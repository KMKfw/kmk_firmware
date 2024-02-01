import usb_cdc

from kmk.keys import make_key
from kmk.modules import Module

# key order from https://github.com/openstenoproject/plover/blob/main/plover/machine/geminipr.py
# do not rearrange
STENO_KEYS = (
    'STN_FN',
    'STN_N1',
    'STN_N2',
    'STN_N3',
    'STN_N4',
    'STN_N5',
    'STN_N6',
    'STN_LS1',
    'STN_LS2',
    'STN_LT',
    'STN_LK',
    'STN_LP',
    'STN_LW',
    'STN_LH',
    'STN_LR',
    'STN_A',
    'STN_O',
    'STN_AS1',
    'STN_AS2',
    'STN_RES1',
    'STN_RES2',
    'STN_PWR',
    'STN_AS3',
    'STN_AS4',
    'STN_E',
    'STN_U',
    'STN_RF',
    'STN_RR',
    'STN_RP',
    'STN_RB',
    'STN_RL',
    'STN_RG',
    'STN_RT',
    'STN_RS',
    'STN_RD',
    'STN_N7',
    'STN_N8',
    'STN_N9',
    'STN_NA',
    'STN_NB',
    'STN_NC',
    'STN_RZ',
)


class Steno(Module):
    def __init__(self):
        self._should_write = False

        self._buffer = bytearray(6)
        self._initialize_buffer()

        for idx, key in enumerate(STENO_KEYS):
            make_key(
                code=((idx // 7) << 8) | (0x40 >> (idx % 7)),
                names=(key,),
                on_press=self._steno_press,
                on_release=self._steno_release,
            )

    def _initialize_buffer(self):
        self._buffer[:] = b'\x80\x00\x00\x00\x00\x00'

    # flip a key's bit in the buffer
    def _steno_press(self, key, *_):
        self._should_write = True
        self._buffer[key.code >> 8] |= key.code & 0xFF

    # send all keys that were pressed, and reset the buffer
    def _steno_release(self, *_):
        if self._should_write:
            usb_cdc.data.write(self._buffer)

            self._should_write = False
            self._initialize_buffer()

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        pass

    def after_matrix_scan(self, keyboard):
        pass

    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass
