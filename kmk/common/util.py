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


def sleep_ms(ms):
    '''
    Tries to sleep for a number of milliseconds in a cross-implementation
    way. Will raise an ImportError if time is not available on the platform.
    '''
    try:
        import time
        time.sleep_ms(ms)
    except AttributeError:
        import time
        time.sleep(ms / 1000)
