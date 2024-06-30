from kmk.extensions import Extension
from kmk.keys import ConsumerKey, make_key


class MediaKeys(Extension):
    def __init__(self):
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
            (0xE2, ('AUDIO_MUTE', 'MUTE')),
            (0xE9, ('AUDIO_VOL_UP', 'VOLU')),
            (0xEA, ('AUDIO_VOL_DOWN', 'VOLD')),
            (0x6F, ('BRIGHTNESS_UP', 'BRIU')),
            (0x70, ('BRIGHTNESS_DOWN', 'BRID')),
            (0xB5, ('MEDIA_NEXT_TRACK', 'MNXT')),
            (0xB6, ('MEDIA_PREV_TRACK', 'MPRV')),
            (0xB7, ('MEDIA_STOP', 'MSTP')),
            (0xCD, ('MEDIA_PLAY_PAUSE', 'MPLY')),
            (0xB8, ('MEDIA_EJECT', 'EJCT')),
            (0xB3, ('MEDIA_FAST_FORWARD', 'MFFD')),
            (0xB4, ('MEDIA_REWIND', 'MRWD')),
        )

        for code, names in codes:
            make_key(names=names, constructor=ConsumerKey, code=code)

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
