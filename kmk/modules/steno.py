from kmk.modules import Module
from kmk.keys import make_key

import usb_cdc

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
        self._initialize_buffer()

        self._codes = {}
        for idx, key in enumerate(STENO_KEYS):
            newKey = make_key(
                names=(key,), on_press=self._steno_press, on_release=self._steno_release
            )
            self._codes[newKey.code] = idx

    def _initialize_buffer(self):
        self._buffer = bytearray(6)
        self._buffer[0] = 0x80

    # flip a key's bit in the buffer
    def _steno_press(self, key, *_):
        idx = self._codes[key.code]
        self._buffer[idx // 7] |= 0x80 >> (idx % 7 + 1)

    # send all keys that were pressed, and reset the buffer
    def _steno_release(self, *_):
        usb_cdc.data.write(self._buffer)
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
