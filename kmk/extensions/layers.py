import kmk.handlers.modtap as modtap
from kmk.extensions import Extension
from kmk.key_validators import layer_key_validator, mod_tap_validator
from kmk.keys import make_argumented_key
from kmk.kmktime import ticks_diff, ticks_ms


class Layers(Extension):
    def __init__(self):
        # Layers
        make_argumented_key(
            validator=layer_key_validator,
            names=('MO',),
            on_press=self.mo_pressed,
            on_release=self.mo_released,
        )
        make_argumented_key(
            validator=layer_key_validator, names=('DF',), on_press=self.df_pressed
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('LM',),
            on_press=self.lm_pressed,
            on_release=self.lm_released,
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('LT',),
            on_press=self.lt_pressed,
            on_release=self.lt_released,
        )
        make_argumented_key(
            validator=layer_key_validator, names=('TG',), on_press=self.tg_pressed
        )
        make_argumented_key(
            validator=layer_key_validator, names=('TO',), on_press=self.to_pressed
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('TT',),
            on_press=self.tt_pressed,
            on_release=self.tt_released,
        )

        make_argumented_key(
            validator=mod_tap_validator,
            names=('MT',),
            on_press=modtap.mt_pressed,
            on_release=modtap.mt_released,
        )

    def df_pressed(self, key, state, *args, **kwargs):
        '''
        Switches the default layer
        '''
        state._active_layers[-1] = key.meta.layer
        return state

    def mo_pressed(self, key, state, *args, **kwargs):
        '''
        Momentarily activates layer, switches off when you let go
        '''
        state._active_layers.insert(0, key.meta.layer)
        return state

    def mo_released(self, key, state, KC, *args, **kwargs):
        # remove the first instance of the target layer
        # from the active list
        # under almost all normal use cases, this will
        # disable the layer (but preserve it if it was triggered
        # as a default layer, etc.)
        # this also resolves an issue where using DF() on a layer
        # triggered by MO() and then defaulting to the MO()'s layer
        # would result in no layers active
        try:
            del_idx = state._active_layers.index(key.meta.layer)
            del state._active_layers[del_idx]
        except ValueError:
            pass

        return state

    def lm_pressed(self, key, state, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        state._hid_pending = True
        # Sets the timer start and acts like MO otherwise
        state._start_time['lm'] = ticks_ms()
        state._keys_pressed.add(key.meta.kc)
        return self.mo_pressed(key, state, *args, **kwargs)

    def lm_released(self, key, state, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        state._hid_pending = True
        state._keys_pressed.discard(key.meta.kc)
        state._start_time['lm'] = None
        return self.mo_released(key, state, *args, **kwargs)

    def lt_pressed(self, key, state, *args, **kwargs):
        # Sets the timer start and acts like MO otherwise
        state._start_time['lt'] = ticks_ms()
        return self.mo_pressed(key, state, *args, **kwargs)

    def lt_released(self, key, state, *args, **kwargs):
        # On keyup, check timer, and press key if needed.
        if state._start_time['lt'] and (
            ticks_diff(ticks_ms(), state._start_time['lt']) < state.tap_time
        ):
            state._hid_pending = True
            state._tap_key(key.meta.kc)

        self.mo_released(key, state, *args, **kwargs)
        state._start_time['lt'] = None
        return state

    def tg_pressed(self, key, state, *args, **kwargs):
        '''
        Toggles the layer (enables it if not active, and vise versa)
        '''
        # See mo_released for implementation details around this
        try:
            del_idx = state._active_layers.index(key.meta.layer)
            del state._active_layers[del_idx]
        except ValueError:
            state._active_layers.insert(0, key.meta.layer)

        return state

    def to_pressed(self, key, state, *args, **kwargs):
        '''
        Activates layer and deactivates all other layers
        '''
        state._active_layers.clear()
        state._active_layers.insert(0, key.meta.layer)

        return state

    def tt_pressed(self, key, state, *args, **kwargs):
        '''
        Momentarily activates layer if held, toggles it if tapped repeatedly
        '''
        # TODO Make this work with tap dance to function more correctly, but technically works.
        if state._start_time['tt'] is None:
            # Sets the timer start and acts like MO otherwise
            state._start_time['tt'] = ticks_ms()
            return self.mo_pressed(key, state, *args, **kwargs)
        elif ticks_diff(ticks_ms(), state._start_time['tt']) < state.tap_time:
            state._start_time['tt'] = None
            return self.tg_pressed(key, state, *args, **kwargs)

    def tt_released(self, key, state, *args, **kwargs):
        tap_timed_out = (
            ticks_diff(ticks_ms(), state._start_time['tt']) >= state.tap_time
        )
        if state._start_time['tt'] is None or tap_timed_out:
            # On first press, works like MO. On second press, does nothing unless let up within
            # time window, then acts like TG.
            state._start_time['tt'] = None
            return self.mo_released(key, state, *args, **kwargs)

        return state
