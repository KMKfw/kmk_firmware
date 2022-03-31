import busio
from analogio import AnalogIn
from supervisor import ticks_ms

from kmk.modules import Module

class BasePotentiometer:
    
    def __init__(self, is_inverted=False):
        self.is_inverted = is_inverted
        self.read_pin = None
        self._state = None
        self._direction = None
        self._pos = 0.0
        self._timestamp = ticks_ms()
        
        # callback function on events. Needs to be defined externally
        self.on_move_do = None
        
    def get_state(self):
        return {
            'direction': self.is_inverted and -self._direction or self._direction,
            'position': self.is_inverted and -self._pos or self._pos,
            'velocity': self._velocity,
        }
        
    def update_state(self):
        new_state = self.read_pin.value
        
        self._direction = 0
        
        if new_state != self._state:
            # movement detected!
            # Debounce...
            
            # AnalogRead always reports 16 bit values
            # convert to percentage and round to hundreths
            new_pos = round(new_state / 0xFFFF, 2)
            
            if new_pos != self._pos:
                self._pos = new_pos
            
                if new_state > self._state:
                    self._direction = 1
                else:
                    self._direction = -1
                    
                if self.on_move_do is not None:
                    self.on_move_do(self.get_state())
              
class GPIOPotentiometer(BasePotentiometer):
    def __init__(self, pin, move_callback, is_inverted = False):
        super().__init__(is_inverted)
        self.read_pin = AnalogIn(pin)
        self.update_state()
        self.cb = move_callback

    def on_move_do(self, state):
        self.cb(state)
        
class PotentiometerHandler(Module):
    def __init__(self):
        self.potentiometers = []
        self.pins = None
    
    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        if self.pins:
            for args in enumerate(self.pins):
                self.potentiometers.append( GPIOPotentiometer(*args) )
        return
    
    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        for encoder in self.encoders:
            encoder.update_state()

        return keyboard

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return