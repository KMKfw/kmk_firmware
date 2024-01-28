from . import DisplayBase


# Intended for displays with drivers built into CircuitPython
# that can be used directly without manual initialization
class BuiltInDisplay(DisplayBase):
    def __init__(self, display=None, sleep_command=None, wake_command=None):
        self.display = display
        self.sleep_command = sleep_command
        self.wake_command = wake_command
        self.is_awake = True

    def during_bootup(self, width, height, rotation):
        self.display.rotation = rotation
        return self.display

    def deinit(self):
        return

    def sleep(self):
        self.display.bus.send(self.sleep_command, b'')

    def wake(self):
        self.display.bus.send(self.wake_command, b'')
