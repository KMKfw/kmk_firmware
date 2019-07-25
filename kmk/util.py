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
