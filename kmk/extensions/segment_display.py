from busio import I2C
try:
    from adafruit_ht16k33 import segments
except:
    print('Wrong version or missing segment Module')

from kmk.extensions import Extension
class Segment(Extension):
    def __init__(
        self,
        SDA,
        SCL,
        toDisplay: str = '0',
        length: int = 2,
    ):
        self._toDisplay = toDisplay
        self._display = segments.Seg7x4(I2C(SCL, SDA))
        self._prevLayers = 0
        self._length = length
        self._display.fill(0)

    def updateSegment(self, sandbox):
        self._toDisplay = '%s' % sandbox.active_layers[0]
        layer_len = len(self._toDisplay)
        for element in range(0, self._length):
            print(element)
            if element >= layer_len:
                self._display[element] = '0'
            else:
                self._display[element]=self._toDisplay[element]

                


    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        self.updateSegment(sandbox)
        return

    def before_matrix_scan(self, sandbox):
        if sandbox.active_layers[0] != self._prevLayers:
            self._prevLayers = sandbox.active_layers[0]
            self.updateSegment(sandbox)
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