'''One layer isn't enough. Adds keys to get to more of them'''
from micropython import const

from kmk.key_validators import layer_key_validator
from kmk.keys import make_argumented_key
from kmk.kmktime import accurate_ticks, accurate_ticks_diff
from kmk.modules import Module


class LayerType:
    '''Defines layer type values for readability'''

    MO = const(0)
    DF = const(1)
    LM = const(2)
    LT = const(3)
    TG = const(4)
    TT = const(5)


class Layers(Module):
    '''Gives access to the keys used to enable the layer system'''

    def __init__(self):
        # Layers
        self.start_time = {
            LayerType.LT: None,
            LayerType.TG: None,
            LayerType.TT: None,
            LayerType.LM: None,
        }
        make_argumented_key(
            validator=layer_key_validator,
            names=('MO',),
            on_press=self._mo_pressed,
            on_release=self._mo_released,
        )
        make_argumented_key(
            validator=layer_key_validator, names=('DF',), on_press=self._df_pressed
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('LM',),
            on_press=self._lm_pressed,
            on_release=self._lm_released,
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('LT',),
            on_press=self._lt_pressed,
            on_release=self._lt_released,
        )
        make_argumented_key(
            validator=layer_key_validator, names=('TG',), on_press=self._tg_pressed
        )
        make_argumented_key(
            validator=layer_key_validator, names=('TO',), on_press=self._to_pressed
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('TT',),
            on_press=self._tt_pressed,
            on_release=self._tt_released,
        )

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

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

    def _df_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Switches the default layer
        '''
        keyboard.active_layers[-1] = key.meta.layer

    def _mo_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Momentarily activates layer, switches off when you let go
        '''
        keyboard.active_layers.insert(0, key.meta.layer)

    @staticmethod
    def _mo_released(key, keyboard, *args, **kwargs):
        # remove the first instance of the target layer
        # from the active list
        # under almost all normal use cases, this will
        # disable the layer (but preserve it if it was triggered
        # as a default layer, etc.)
        # this also resolves an issue where using DF() on a layer
        # triggered by MO() and then defaulting to the MO()'s layer
        # would result in no layers active
        try:
            del_idx = keyboard.active_layers.index(key.meta.layer)
            del keyboard.active_layers[del_idx]
        except ValueError:
            pass

    def _lm_pressed(self, key, keyboard, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        keyboard.hid_pending = True
        # Sets the timer start and acts like MO otherwise
        keyboard.keys_pressed.add(key.meta.kc)
        self._mo_pressed(key, keyboard, *args, **kwargs)

    def _lm_released(self, key, keyboard, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        keyboard.hid_pending = True
        keyboard.keys_pressed.discard(key.meta.kc)
        self._mo_released(key, keyboard, *args, **kwargs)

    def _lt_pressed(self, key, keyboard, *args, **kwargs):
        # Sets the timer start and acts like MO otherwise
        self.start_time[LayerType.LT] = accurate_ticks()
        self._mo_pressed(key, keyboard, *args, **kwargs)

    def _lt_released(self, key, keyboard, *args, **kwargs):
        # On keyup, check timer, and press key if needed.
        if self.start_time[LayerType.LT] and (
            accurate_ticks_diff(
                accurate_ticks(), self.start_time[LayerType.LT], keyboard.tap_time
            )
        ):
            keyboard.hid_pending = True
            keyboard.tap_key(key.meta.kc)

        self._mo_released(key, keyboard, *args, **kwargs)
        self.start_time[LayerType.LT] = None

    def _tg_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Toggles the layer (enables it if not active, and vise versa)
        '''
        # See mo_released for implementation details around this
        try:
            del_idx = keyboard.active_layers.index(key.meta.layer)
            del keyboard.active_layers[del_idx]
        except ValueError:
            keyboard.active_layers.insert(0, key.meta.layer)

    def _to_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Activates layer and deactivates all other layers
        '''
        keyboard.active_layers.clear()
        keyboard.active_layers.insert(0, key.meta.layer)

    def _tt_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Momentarily activates layer if held, toggles it if tapped repeatedly
        '''
        if self.start_time[LayerType.TT] is None:
            # Sets the timer start and acts like MO otherwise
            self.start_time[LayerType.TT] = accurate_ticks()
            self._mo_pressed(key, keyboard, *args, **kwargs)
        elif accurate_ticks_diff(
            accurate_ticks(), self.start_time[LayerType.TT], keyboard.tap_time
        ):
            self.start_time[LayerType.TT] = None
            self._tg_pressed(key, keyboard, *args, **kwargs)
            return
        return

    def _tt_released(self, key, keyboard, *args, **kwargs):
        if self.start_time[LayerType.TT] is None or not accurate_ticks_diff(
            accurate_ticks(), self.start_time[LayerType.TT], keyboard.tap_time
        ):
            # On first press, works like MO. On second press, does nothing unless let up within
            # time window, then acts like TG.
            self.start_time[LayerType.TT] = None
            self._mo_released(key, keyboard, *args, **kwargs)
