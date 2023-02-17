'''One layer isn't enough. Adds keys to get to more of them'''
from kmk.keys import KC, make_argumented_key
from kmk.modules.holdtap import HoldTap, HoldTapKeyMeta
from kmk.utils import Debug

debug = Debug(__name__)


def layer_key_validator(layer, kc=None):
    '''
    Validates the syntax (but not semantics) of a layer key call.  We won't
    have access to the keymap here, so we can't verify much of anything useful
    here (like whether the target layer actually exists). The spirit of this
    existing is mostly that Python will catch extraneous args/kwargs and error
    out.
    '''
    return LayerKeyMeta(layer, kc)


def layer_key_validator_lt(layer, kc, prefer_hold=False, **kwargs):
    return HoldTapKeyMeta(tap=kc, hold=KC.MO(layer), prefer_hold=prefer_hold, **kwargs)


def layer_key_validator_tt(layer, prefer_hold=True, **kwargs):
    return HoldTapKeyMeta(
        tap=KC.TG(layer), hold=KC.MO(layer), prefer_hold=prefer_hold, **kwargs
    )


class LayerKeyMeta:
    def __init__(self, layer, kc=None):
        self.layer = layer
        self.kc = kc


class Layers(HoldTap):
    '''Gives access to the keys used to enable the layer system'''

    def __init__(self):
        # Layers
        super().__init__()
        make_argumented_key(
            validator=layer_key_validator,
            names=('MO',),
            on_press=self._mo_pressed,
            on_release=self._mo_released,
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('DF',),
            on_press=self._df_pressed,
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('LM',),
            on_press=self._lm_pressed,
            on_release=self._lm_released,
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('TG',),
            on_press=self._tg_pressed,
        )
        make_argumented_key(
            validator=layer_key_validator,
            names=('TO',),
            on_press=self._to_pressed,
        )
        make_argumented_key(
            validator=layer_key_validator_lt,
            names=('LT',),
            on_press=self.ht_pressed,
            on_release=self.ht_released,
        )
        make_argumented_key(
            validator=layer_key_validator_tt,
            names=('TT',),
            on_press=self.ht_pressed,
            on_release=self.ht_released,
        )

    def _df_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Switches the default layer
        '''
        keyboard.active_layers[-1] = key.meta.layer
        self._print_debug(keyboard)

    def _mo_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Momentarily activates layer, switches off when you let go
        '''
        keyboard.active_layers.insert(0, key.meta.layer)
        self._print_debug(keyboard)

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
        __class__._print_debug(__class__, keyboard)

    def _lm_pressed(self, key, keyboard, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        # Sets the timer start and acts like MO otherwise
        keyboard.add_key(key.meta.kc)
        self._mo_pressed(key, keyboard, *args, **kwargs)

    def _lm_released(self, key, keyboard, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        keyboard.remove_key(key.meta.kc)
        self._mo_released(key, keyboard, *args, **kwargs)

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

    def _print_debug(self, keyboard):
        # debug(f'__getitem__ {key}')
        if debug.enabled:
            debug(f'active_layers={keyboard.active_layers}')
