try:
    import machine

    machine.bootloader()

except ImportError:
    import microcontroller

    microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
    microcontroller.reset()
