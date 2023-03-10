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

    _active_combo = None

    def __init__(
        self,
        combo_layers=None,
    ):
        # Layers
        super().__init__()
        self.combo_layers = combo_layers
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
            validator=layer_key_validator, names=('TG',), on_press=self._tg_pressed
        )
        make_argumented_key(
            validator=layer_key_validator, names=('TO',), on_press=self._to_pressed
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
        self.activate_layer(keyboard, key.meta.layer, as_default=True)

    def _mo_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Momentarily activates layer, switches off when you let go
        '''
        self.activate_layer(keyboard, key.meta.layer)

    def _mo_released(self, key, keyboard, *args, **kwargs):
        self.deactivate_layer(keyboard, key.meta.layer)

    def _lm_pressed(self, key, keyboard, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        keyboard.hid_pending = True
        keyboard.keys_pressed.add(key.meta.kc)
        self.activate_layer(keyboard, key.meta.layer)

    def _lm_released(self, key, keyboard, *args, **kwargs):
        '''
        As MO(layer) but with mod active
        '''
        keyboard.hid_pending = True
        keyboard.keys_pressed.discard(key.meta.kc)
        self.deactivate_layer(keyboard, key.meta.layer)

    def _tg_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Toggles the layer (enables it if not active, and vise versa)
        '''
        # See mo_released for implementation details around this
        if key.meta.layer in keyboard.active_layers:
            self.deactivate_layer(keyboard, key.meta.layer)
        else:
            self.activate_layer(keyboard, key.meta.layer)

    def _to_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Activates layer and deactivates all other layers
        '''
        self._active_combo = None
        keyboard.active_layers.clear()
        keyboard.active_layers.insert(0, key.meta.layer)

    def _print_debug(self, keyboard):
        if debug.enabled:
            debug(f'active_layers={keyboard.active_layers}')

    def activate_layer(self, keyboard, layer, as_default=False):
        if as_default:
            keyboard.active_layers[-1] = layer
        else:
            keyboard.active_layers.insert(0, layer)

        if self.combo_layers:
            self._activate_combo_layer(keyboard)

        self._print_debug(keyboard)

    def deactivate_layer(self, keyboard, layer):
        # Remove the first instance of the target layer from the active list
        # under almost all normal use cases, this will disable the layer (but
        # preserve it if it was triggered as a default layer, etc.).
        # This also resolves an issue where using DF() on a layer
        # triggered by MO() and then defaulting to the MO()'s layer
        # would result in no layers active.
        try:
            del_idx = keyboard.active_layers.index(layer)
            del keyboard.active_layers[del_idx]
        except ValueError:
            if debug.enabled:
                debug(f'_mo_released: layer {layer} not active')

        if self.combo_layers:
            self._deactivate_combo_layer(keyboard, layer)

        self._print_debug(keyboard)

    def _activate_combo_layer(self, keyboard):
        if self._active_combo:
            return

        for combo, result in self.combo_layers.items():
            matching = True
            for layer in combo:
                if layer not in keyboard.active_layers:
                    matching = False
                    break

            if matching:
                self._active_combo = combo
                keyboard.active_layers.insert(0, result)
                break

    def _deactivate_combo_layer(self, keyboard, layer):
        if self._active_combo and layer in self._active_combo:
            keyboard.active_layers.remove(self.combo_layers[self._active_combo])
            self._active_combo = None
