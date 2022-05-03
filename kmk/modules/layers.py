'''One layer isn't enough. Adds keys to get to more of them'''
from kmk.key_validators import layer_key_validator
from kmk.keys import KC, make_argumented_key
from kmk.modules.holdtap import ActivationType, HoldTap
from kmk.types import HoldTapKeyMeta


def layer_key_validator_lt(layer, kc, prefer_hold=False, **kwargs):
    return HoldTapKeyMeta(tap=kc, hold=KC.MO(layer), prefer_hold=prefer_hold, **kwargs)


def layer_key_validator_tt(layer, prefer_hold=True, **kwargs):
    return HoldTapKeyMeta(
        tap=KC.TG(layer), hold=KC.MO(layer), prefer_hold=prefer_hold, **kwargs
    )


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

    def process_key(self, keyboard, key, is_pressed, int_coord):
        current_key = super().process_key(keyboard, key, is_pressed, int_coord)

        for key, state in self.key_states.items():
            if key == current_key:
                continue

            # on interrupt: key must be translated here, because it was asigned
            # before the layer shift happend.
            if state.activated == ActivationType.INTERRUPTED:
                current_key = keyboard._find_key_in_map(int_coord)

        return current_key

    def send_key_buffer(self, keyboard):
        for (int_coord, old_key) in self.key_buffer:
            new_key = keyboard._find_key_in_map(int_coord)

            # adding keys late to _coordkeys_pressed isn't pretty,
            # but necessary to mitigate race conditions when multiple
            # keys are pressed during a tap-interrupted hold-tap.
            keyboard._coordkeys_pressed[int_coord] = new_key
            new_key.on_press(keyboard)

            keyboard._send_hid()

        self.key_buffer.clear()

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
