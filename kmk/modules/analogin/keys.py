from . import AnalogEvent


class AnalogKey(AnalogEvent):
    def __init__(self, key, threshold=127):
        self.key = key
        self.threshold = threshold
        self.pressed = False

    def on_change(self, event, keyboard):
        if event.value >= self.threshold and not self.pressed:
            self.pressed = True
            keyboard.pre_process_key(self.key, True)

        elif event.value < self.threshold and self.pressed:
            self.pressed = False
            keyboard.pre_process_key(self.key, False)

    def on_stop(self, event, keyboard):
        pass
