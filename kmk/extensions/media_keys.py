from kmk.extensions import Extension
from kmk.keys import KC, make_consumer_key


class MediaKeys(Extension):
    def __init__(self):
        KC._generators.append(self.maybe_make_media_key)

    @staticmethod
    def maybe_make_media_key(candidate):
        # Consumer ("media") keys. Most known keys aren't supported here. A much
        # longer list used to exist in this file, but the codes were almost certainly
        # incorrect, conflicting with each other, or otherwise 'weird'. We'll add them
        # back in piecemeal as needed. PRs welcome.
        #
        # A super useful reference for these is http://www.freebsddiary.org/APC/usb_hid_usages.php
        # Note that currently we only have the PC codes. Recent MacOS versions seem to
        # support PC media keys, so I don't know how much value we would get out of
        # adding the old Apple-specific consumer codes, but again, PRs welcome if the
        # lack of them impacts you.
        codes = (
            (226, ('AUDIO_MUTE', 'MUTE')),  # 0xE2
            (233, ('AUDIO_VOL_UP', 'VOLU')),  # 0xE9
            (234, ('AUDIO_VOL_DOWN', 'VOLD')),  # 0xEA
            (111, ('BRIGHTNESS_UP', 'BRIU')),  # 0x6F
            (112, ('BRIGHTNESS_DOWN', 'BRID')),  # 0x70
            (181, ('MEDIA_NEXT_TRACK', 'MNXT')),  # 0xB5
            (182, ('MEDIA_PREV_TRACK', 'MPRV')),  # 0xB6
            (183, ('MEDIA_STOP', 'MSTP')),  # 0xB7
            (205, ('MEDIA_PLAY_PAUSE', 'MPLY')),  # 0xCD (this may not be right)
            (184, ('MEDIA_EJECT', 'EJCT')),  # 0xB8
            (179, ('MEDIA_FAST_FORWARD', 'MFFD')),  # 0xB3
            (180, ('MEDIA_REWIND', 'MRWD')),  # 0xB4
        )
        for code, names in codes:
            if candidate in names:
                return make_consumer_key(code=code, names=names)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
