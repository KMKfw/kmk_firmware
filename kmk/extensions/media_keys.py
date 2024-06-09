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

        make_key(code=0xE2, names=('AUDIO_MUTE', 'MUTE'), key_type=ConsumerKey)
        make_key(code=0xE9, names=('AUDIO_VOL_UP', 'VOLU'), key_type=ConsumerKey)
        make_key(code=0xEA, names=('AUDIO_VOL_DOWN', 'VOLD'), key_type=ConsumerKey)
        make_key(code=0x6F, names=('BRIGHTNESS_UP', 'BRIU'), key_type=ConsumerKey)
        make_key(code=0x70, names=('BRIGHTNESS_DOWN', 'BRID'), key_type=ConsumerKey)
        make_key(code=0xB5, names=('MEDIA_NEXT_TRACK', 'MNXT'), key_type=ConsumerKey)
        make_key(code=0xB6, names=('MEDIA_PREV_TRACK', 'MPRV'), key_type=ConsumerKey)
        make_key(code=0xB7, names=('MEDIA_STOP', 'MSTP'), key_type=ConsumerKey)
        make_key(code=0xCD, names=('MEDIA_PLAY_PAUSE', 'MPLY'), key_type=ConsumerKey)
        make_key(code=0xB8, names=('MEDIA_EJECT', 'EJCT'), key_type=ConsumerKey)
        make_key(code=0xB3, names=('MEDIA_FAST_FORWARD', 'MFFD'), key_type=ConsumerKey)
        make_key(code=0xB4, names=('MEDIA_REWIND', 'MRWD'), key_type=ConsumerKey)

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
