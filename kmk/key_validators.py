from kmk.types import KeySeqSleepMeta, UnicodeModeKeyMeta


def key_seq_sleep_validator(ms):
    return KeySeqSleepMeta(ms)


def unicode_mode_key_validator(mode):
    return UnicodeModeKeyMeta(mode)
