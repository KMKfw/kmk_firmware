from analogio import AnalogIn
from keypad import Event as KeyEvent
from kmk.scanners import Scanner


class AnalogKeyScanner(Scanner):
    def __init__(self,
        pin_map,
        invert=False,
        threshold_map = [],
        offset=0,
        filter = lambda input: input.value >> 8, #shifts input to [0-255]
    ):
        self.pin_map = pin_map
        
        self.invert = invert
        self.offset = offset
        self.filter = filter
        self._key_count = len(pin_map)
        #having invert prevents some phantom presses during boot
        self.state = [self.invert] * self._key_count 
        self.analog = []

        if len(threshold_map) == 0:
            self.threshold_map = [127]*self._key_count
        else:
            self.threshold_map = threshold_map
            
        for index, pin in enumerate(self.pin_map):
            self.analog.append(AnalogIn(pin))
        

    @property
    def key_count(self):
        return self.key_count

    def scan_for_changes(self):
        any_changed = False
        for key_num, analog in enumerate(self.analog):
            
            value = self.filter(analog)

            if value < self.threshold_map[key_num]:
                pressed = True
            else:
                pressed = False

            if pressed != self.state[key_num]:
                any_changed = True
                self.state[key_num] = pressed
                
            if any_changed:
                break


        if self.invert:
            pressed = not pressed

        if any_changed:
            key_number = self.offset + key_num
            return KeyEvent(key_number,pressed)

                                
#wip
#class AnalogMuxKeyScanner(Scanner):
#    def __init__(self,i2c_pin


#could be usefull for other stuff
#out of scope... again missed point of this
        ## invert the filter by changing the outputed value to a negitive then adding back to positive
        ## and getting max val from the filter so even very custom filters can work
##        if self.invert:
##            filtermax = filter(65535) + 1 #eval filter max to not run every time
##            self.filter = lambda input:((~filter) + filtermax)
##        else:
##            self.filter = filter
