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




## invert the filter by changing the outputed value to a negitive then adding back to positive
## and getting max val from the filter so even very custom filters can work
def eval_filter(filter, invert):
    if invert == True:
        filter_max = filter(65535) + 1 #eval filter max to not run every time
        filter_out = lambda input: ((~filter(input)) + filter_max)
    else:
        filter_out = filter
        filter_max = 255
    return filter_out, filter_max





#class to provide on_change and on_stop if not
#found diverts to noop
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

    #the threshold is setup so 0 is at the top of switch
    #this is mainly to match the normal bool state of switches
    #with 0 being off and 1 being being pressed 
    def on_change(self, keyboard, analog):
        debug(analog.value)
        if analog.value >= self.threshold and not self.pressed:
            self.pressed = True
            keyboard.pre_process_key(self.key, True)

        elif analog.value < self.threshold and self.pressed:
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
        self.filter, self.filtermax = eval_filter(filter, self.invert)
        self._state = False
        self.raw_value = 0
        self.time = ticks_ms()
        self.value = 0
        self.delta = 0
        

    #calculate velocity upon call, this is kept serpate
    #so as to not waste time with an unnecessary calc unless needed
    #other expressions that could be common usecases could be added
    #in a simalar vein to this however I can't think of anything that a
    #external function could not do on it's own with the info provided
    #VEL_MAX_TIME might need to be calibraded per keyboard config
    #this mainly depends on the micro-controler and loaded modules
    #more testing needed
    @property 
    def velocity(self):
        #this exprestion should allow for velocity to be from
        #0 to the max val of the filter (then we clamp it)
        #this should give a good representation of the velocity
        #but scaled to somthing that would be more useful to a function
        velocity = min(
            max(0,
                int(
                    self.delta / (ticks_ms() - self.time)* self.filtermax / VEL_MAX_TIME
                    )
                ),
            self.filtermax
            )
        return velocity


    #does what it says on the tin and updates the state of
    #value. time, delta, _state
    #time is not used in this but it is used in velocity and
    #could be used in other functions (not sure for what but it's there)
    def update_state(self):
        value = self.filter(self.input())
        delta = value - self.value

        #randomly takes ~27ms (likely due to the garbage colector or other threads)
        if delta not in range(-self.sensitivity, self.sensitivity + 1):
            self.value = value #catch slow movements by not updating until delta passed
            self._state = True
            
            
        elif (delta in range(-self.sensitivity, self.sensitivity + 1) and
              self.delta not in range(-self.sensitivity, self.sensitivity + 1)):
            self.value = value
            self._state = False
        
        
        self.delta = delta
        self.time = ticks_ms()


        
    #WIP
    #for external compatable functions to use to recalc using custom values
    def ext_handler(self, function_filter, function_sensitivity):
        print("null")
        #things to return
        #recomputed value if user has not set their own filter for that input




class MuxedAnlogInput:
     def __init__(self,idx):
         print("tmp")


#Main interface for the user 
#arrays like filtermap, invertmap, and sensitivitymap auto fill if they only have one entry
#I don't like how big invert map could be for what it is so perhaps it could be a true bitmap
#but I also need to add perlayer functionaltiy to the 3 maps and AnalogInput so perhaps it
#might be worth it.
#I broke out the state var so it could be used as an event trigger to allow for
#the rest of kmk to run mor async but don't know how best to do this efficiently or
#within the kmk scope
#biggest problem is duplicated information that is only used once in the handler
#not sure what the best way to deal with this is other than passing it from handler live
#that could work for anything that needs layermaping I guess but I also don't want the user to
#have to make masive arrays just to use invert differently on one layer
#perhaps a more complex parcer is needed during bootup
#need to add catches for no event, a KC on it's own
class AnalogHandler(Module):
    def __init__(self):
        self.analogs = []                 #array of analogs to call during runtime
        self.apins = None                 #analog pins (required)
        self.evtmap = None                #event map of inputs (required) (2d array like a keymap)
        self.mpins = None                 #muxing  pins (optional)
        self.disabledmuxs = None          #list of disabled mux keys
                                          #(so you don't have a bunch of floating or grounded keys)
                                          #list of indexs to skip during boot (might need a better solution)
        self.filtermap = [DEFAULT_FILTER] #list to contain custom filters to the inputs
        self.invertmap = [False]          #list to set inputs to be inverted or all
        self.sensitivitymap = [1]         #set the sensitivity of each input
        
    def on_runtime_enable(self, keyboard):
        return

    def on_runtime_disable(self, keyboard):
        return


    #look into getting filters from event func and passing those at runtime
    #so filters can be per layer
    def during_bootup(self, keyboard):
        if self.apins and self.evtmap:
            if self.mpins is not None:
                #pass to mux handler
                print("not implemented yet")
            else:
                #direct pin mode
                #perhaps move to func?
                if debug.enabled:
                    debug('analog mode: direct pin mode')
                for idx, pin in enumerate(self.apins):
                    #allow for filter, invert and sensitivity to be either fill all or per io
                    #might compact this.. looks ugly
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

                    self.analogs.append(
                        AnalogInput(AnalogIn(pin),filter, invert, sensitivity)
                    )
                    
                print(self.analogs)
        elif debug.enabled:
            debug('missing event map or analog pins')
            
        return


    #perhaps for update_state it could takeing the filter from the external list
    #honisly should look into running the external func to get it's info
    #like filters during boot up
    def before_matrix_scan(self, keyboard):
        for idx, analog in enumerate(self.analogs):
            #timein = ticks_ms()
            old_state = analog._state
            analog.update_state()
         
            event_func = self.evtmap[keyboard.active_layers[0]][idx]

            if analog._state: #on change
                
                event_func.on_change(keyboard, analog)
            elif not analog._state and old_state: #on stop
                event_func.on_stop(keyboard, analog)
            #else: it hasen't moved so no reason to do anything
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
