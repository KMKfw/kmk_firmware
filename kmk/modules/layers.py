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

    def __init__(
        self,
        combolayers=None,
    ):
        # Layers
        super().__init__()
        self.combolayers = combolayers
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
        keyboard.active_layers[-1] = key.meta.layer
        self._print_debug(keyboard)

    def _mo_pressed(self, key, keyboard, *args, **kwargs):
        '''
        Momentarily activates layer, switches off when you let go
        '''
        if self.combolayers is None:
            keyboard.active_layers.insert(0, key.meta.layer)
            self._print_debug(keyboard)
        else:
            keyboard.active_layers.insert(0, key.meta.layer)
            combo_result = self.get_combo_layer(keyboard)
            if combo_result:
                keyboard.active_layers.insert(0, combo_result)
            self._print_debug(keyboard)

    # @staticmethod
    def _mo_released(self, key, keyboard, *args, **kwargs):
        # remove the first instance of the target layer
        # from the active list
        # under almost all normal use cases, this will
        # disable the layer (but preserve it if it was triggered
        # as a default layer, etc.)
        # this also resolves an issue where using DF() on a layer
        # triggered by MO() and then defaulting to the MO()'s layer
        # would result in no layers active
        if self.combolayers is None:
            try:
                del_idx = keyboard.active_layers.index(key.meta.layer)
                del keyboard.active_layers[del_idx]
            except ValueError:
                pass
        else:
            try:
                del_idx = keyboard.active_layers.index(key.meta.layer)
                del keyboard.active_layers[del_idx]
                self._print_debug(keyboard)
                self.remove_combo_layer(keyboard)
                keyboard.active_layers.sort(reverse=True)

            except ValueError:
                pass
        __class__._print_debug(__class__, keyboard)

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

    def get_combo_layer(self, keyboard):

        acvlyrs = []

        # If the active keyboard.active_layers value is greater than 0, then add it to the acvlyrs list
        if len(keyboard.active_layers) > 0:
            for i in keyboard.active_layers:
                if i > 0:
                    acvlyrs.append(i)

            acvlyrs.sort()

            # if the acvlyrs list has more than one item, look for a match in the layerstate dict, if there is a match, make the keyboard.active_layers the 3rd item in the tuple
            if len(acvlyrs) > 1:
                for key, val in self.combolayers.items():
                    if acvlyrs == list(key):
                        return val

    def remove_combo_layer(self, keyboard):

        acvlyrs = []
        cmblyrs = []
        for key, val in self.combolayers.items():
            cmblyrs.append(val)
        if len(keyboard.active_layers) > 1:
            for al in keyboard.active_layers:
                if cmblyrs.count(al) == 0:
                    if acvlyrs.count(al) == 0:
                        acvlyrs.append(al)
                        keyboard.active_layers.remove(al)
                else:
                    keyboard.active_layers.remove(al)

            acvlyrs.sort()

        for al in acvlyrs:
            keyboard.active_layers.insert(0, al)
