def get_wide_ordinal(char):
    if len(char) != 2:
        return ord(char)

    return 0x10000 + (ord(char[0]) - 0xD800) * 0x400 + (ord(char[1]) - 0xDC00)


def flatten_dict(d):
    items = {}

    for k, v in d.items():
        if isinstance(v, dict):
            items.update(flatten_dict(v))
        else:
            items[k] = v

    return items


def reset_keyboard():
    try:
        import machine
        machine.reset()

    except ImportError:
        import microcontroller
        microcontroller.reset()


def reset_bootloader():
    try:
        import machine
        machine.bootloader()

    except ImportError:
        import microcontroller
        microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
        microcontroller.reset()
