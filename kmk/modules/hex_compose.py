from kmk.modules import Module
from kmk.keys import KC, make_key
from kmk.handlers.sequences import unicode_string_sequence


_ascii7_keys = []
for c in range(64, 96):
    _ascii7_keys.append(KC.LCTRL(KC.get(chr(c))))
for c in range(32, 127):
    k = KC.get(chr(c))
    _ascii7_keys.append(KC.LSHIFT(k) if 65 <= c <= 90 else k)
_ascii7_keys.append(KC.DEL)

assert len(_ascii7_keys) == 128, "Failed to enumerate 7-bit ascii keys"


def _utf8_length(first_byte):
    # utf8 encodes length in first byte see https://en.wikipedia.org/wiki/UTF-8
    length = 0
    if first_byte & 0x80 == 0:        # 0xxx xxxx
        length = 1
    elif first_byte & 0xe0 == 0xc0:   # 110x xxxx
        length = 2
    elif first_byte & 0xf0 == 0xe0:   # 1110 xxxx
        length = 3
    elif first_byte & 0xf8 == 0xf0:   # 1111 0xxx
        length = 4
    return length or None


class HexCompose(Module):
    def __init__(self, encoding='utf8'):
        self.encoding = encoding
        self._hex_keys = [
            make_key(
                names=(f'HEX{digit:x}'.upper(), ),
                meta=digit,
            )
            for digit in range(16)
        ]
        self.reset()

    def reset(self):
        self._bytes_needed = 1  # ascii always needs 1, uft8 sets dynamically
        self._hi_nibble = None  # two hex digits => one byte
        self._bytes = b''

    def during_bootup(self, keyboard):
        self.reset()

    def before_matrix_scan(self, keyboard):
        return

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

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if key not in self._hex_keys:
            self.reset()
            return key
        elif not is_pressed:
            return None
        
        digit = key.meta
        print("HexCompose: got hex key", digit)

        # half way thru a byte?  
        if self._hi_nibble is None:
            self._hi_nibble = digit << 4
            return None
                
        # otherwise add a byte
        self._bytes += bytes([self._hi_nibble + digit])
        self._hi_nibble = None

        # validate length and continuation for utf-8
        if self.encoding == 'utf8':
            if len(self._bytes) == 1:
                self._bytes_needed = _utf8_length(self._bytes[0])
                # valid starting byte?
                if not self._bytes_needed:
                    print(f'HexCompose: invalid utf-8 length coding from {self._bytes}')
                    self.reset()
                    return None
            else:
                # valid continuation byte?
                if self._bytes[-1] & 0xc0 != 0x80:
                    print(f'HexCompose: invalid utf-8 continuation in {self._bytes}')
                    self.reset()
                    return None
                
        if len(self._bytes) != self._bytes_needed:
            return None
        
        print('HexCompose: completed bytes', self._bytes)
        character = self._bytes.decode(self.encoding)[0]
        c = ord(character)
        if c < 128:
            composed_key = _ascii7_keys[c]
            print('HexCompose: sending ascii7', composed_key)
        else:
            composed_key = unicode_string_sequence(character)
            print('HexCompose: sending unicode for', character, composed_key)

        self.reset()        

        return composed_key