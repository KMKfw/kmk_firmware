try:
    import machine

    machine.reset()

except ImportError:
    import microcontroller

    microcontroller.reset()
