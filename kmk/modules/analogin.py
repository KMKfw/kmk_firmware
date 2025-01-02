from kmk.keys import KC
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)

DEFAULT_FILTER = lambda input: input >> 8


#thinking notes for mux
#muxing uses dio pins for ch select. while if you have multiple muxers they should all use the same ch select
#some might not follow this. the option should be provided to map seperate pins for each adc
#while there should not be a max to the number of channels there might be a true scanning max before delay holds
#other systems to fault (not sure if this could be threaded or if kmk uses threding to help but if you need
#32 switches on one adc you have a big board or... a big midi pad...)


def noop(*args):
    pass


class AnalogEvent:
    def __init__(self, on_change=noop, on_stop=noop):
        self._on_change = on_change
        self._on_stop = on_stop

    def on_change(self, event, keyboard):
        self._on_change(self, event, keyboard)

    def on_stop(self, event, keyboard):
        self._on_stop(self, event, keyboard)


class AnalogKey(AnalogEvent):
    def __init__(self, key, threshold=127):
        self.key = key
        self.threshold = threshold
        self.pressed = False

    def on_change(self, event, keyboard):
        debug(event.value)
        if event.value >= self.threshold and not self.pressed:
            self.pressed = True
            keyboard.pre_process_key(self.key, True)

        elif event.value < self.threshold and self.pressed:
            self.pressed = False
            keyboard.pre_process_key(self.key, False)

    def on_stop(self, event, keyboard):
        pass


class AnalogInput:
    def __init__(self, input, filter=DEFAULT_FILTER, invert=False, sensitivity=1):
        self.input = input
        self.value = 0
        self.delta = 0
        self.invert = invert
        self.sensitivity = sensitivity

        ## invert the filter by changing the outputed value to a negitive then adding back to positive
        ## and getting max val from the filter so even very custom filters can work
        if self.invert == True:
            print("here")
            filtermax = filter(65535) + 1 #eval filter max to not run every time
            print("not")
            self.filter = lambda input:((~filter) + filtermax)
        else:
            self.filter = filter

    def update_state(self, idx):
        print("updating")
        value = self.filter(self.input)
        self.delta = value - self.value
        if self.delta not in range(-self.sensitivity, self.sensitivity):
            self.value = value
            self.on_move_do(idx)
            



class MuxedAnlogInput:
     def __init__(self,idx):
         print("tmp")

## 
##def update(self):
##        '''
##        Read a new value from an analogio compatible input, apply
##        transformation, then return either the new value if it changed or `None`
##        otherwise.
##        '''
##
##        


##        for idx, input in enumerate(self.inputs):
##            value = input.update()
##
##            # No change in value: stop or pass
##            if value is None:
##                if input in self._active:
##                    if debug.enabled:
##                        debug('on_stop', input, self._active[idx])
##                    self._active[idx].on_stop(input, keyboard)
##                    del self._active[idx]
##                continue
##
##            # Resolve event handler
##            if input in self._active:
##                key = self._active[idx]
##            else:
##                key = None
##                for layer in keyboard.active_layers:
##                    try:
##                        key = self.evtmap[layer][idx]
##                    except IndexError:
##                        if debug.enabled:
##                            debug('evtmap IndexError: idx=', idx, ' layer=', layer)
##                    if key and key != KC.TRNS:
##                        break
##
##            if key == KC.NO:
##                continue
##
##            # Forward change to event handler
##            try:
##                self._active[idx] = key
##                if debug.enabled:
##                    debug('on_change', input, key, value)
##                key.on_change(input, keyboard)
##            except Exception as e:
##                if debug.enabled:
##                    debug(type(e), ': ', e, ' in ', key.on_change)
##



class AnalogHandler(Module):
    def __init__(
         self,
         apins,
         mpins = [],
         disabledmuxs = [],
         evtmap,
         invertmap = [False],
         filtermap = [DEFAULT_FILTER],
         sensitivitymap =[1]
         ):
        
        self.analogs = []
        self.apins = apins #Take in chosen analog pins
        self.mpins = mpins #pins for muxing interface
        self.disabledmuxs = emuxs #2d array containing enabled mux ports per layer
        self.evtmap = evtmap  #event mapping for inputs
        self.filtermap = filtermap # filter array: all same if only first slot filled
        self.invertmap = invertmap # simple bool array for inverting either all if only first slot filled
        self.sensitivitymap = sensitivitymap
        
    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return

    def on_move_do(self, keyboard, idx):
        print(idx)
        print(self.value)
    
    def during_bootup(self, keyboard):
        if self.apins and self.evtmap:
            if len(self.mpins) > 0:
                #pass to mux handler
                print("not implemented yet")
            else:
                #direct pin mode
                for idx, pin in enumerate(self.apins):
                    #allow for filter and invert to be either fill all or per io
                    if len(self.filtermap) > 1:
                        filter = self.filtermap[idx]
                    else:
                        filter = self.filtermap[0]

                    if len(self.invertmap) > 1:
                        invert = self.invertmap[idx]
                    else:
                        invert = self.invertmap[0]

                    if len(self.sensitivitymap) > 1:
                        sensitivity = self.sensitivitymap[idx]
                    else:
                        sensitivity = self.sensitivitymap[0]

                    self.analogs.append
                    (
                        AnalogInput(AnalogIn(pin),filter, invert, sensitivity)
                    )
        return

    def before_matrix_scan(self, keyboard):
        for idx, analog in enumerate self.analogs:
            analog.update_state(idx)
        return keyboard
        
        


    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
