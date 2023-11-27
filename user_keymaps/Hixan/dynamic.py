#!/usr/bin/env python3
import board

from kb import KMKKeyboard
import configuration

from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
from kmk.modules.layers import Layers as _Layers
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.handlers.sequences import simple_key_sequence
import busio as io
import math

keyboard = KMKKeyboard()

class CustomKey:
    SUPPORTED = set()

class CustomLayerKey(CustomKey):
    SUPPORTED = {'MO', 'TG', 'TO', 'DF', 'TT'}
    def __init__(self, attrib, layer=None, extra_args=dict()):
        '''
        action:
        one of set, only, toggle
        '''
        assert attrib in self.SUPPORTED
        print(attrib)
        self._attrib = attrib
        self._layer = layer
        self._extra_args = extra_args

    def __call__(self, layer, **args):
        return CustomLayerKey(self._attrib, layer, extra_args=args)

    def code(self, *, all_layers, **kwargs):
        assert self._layer is not None, "must call CustomLayerKey with the layer you want."
        assert self._layer in all_layers, f"{self._layer=} not in {all_layers=}"
        return getattr(KC, self._attrib)(all_layers.index(self._layer), **self._extra_args)

    def __repr__(self):
        return f"CustomLayerKey(attrib={self._attrib}, layer={self._layer})"

class MapTransformLayerKey(CustomKey):
    SUPPORTED = {'MMO',   'MTG',  'MTO',  'MDF',  'MTT',
                 'UMMO', 'UMTG', 'UMTO', 'UMDF', 'UMTT'}

    def _transform_layer_name(self, layer_name: str):
        return layer_name + '_' + self._suffix

    def _untransform_layer_name(self, layer_name: str):
        assert layer_name.endswith('_' + self._suffix), f"{self=} {layer_name=}"
        return layer_name[:-len(self._suffix) - 1]

    def __init__(self, attrib, suffix=None, extra_args=dict()):
        ''' apply mapping to kv pair. '''
        self._suffix = suffix
        self._attrib = attrib
        self._default_kc = KC.NO
        self._extra_args = extra_args

    def __call__(self, suffix, **extra_args):
        return MapTransformLayerKey(suffix=suffix, attrib=self._attrib, extra_args=extra_args)

    def code(self, *, all_layers, this_layer, **kwargs):
        if self._attrib.startswith('U'):
            transformed_name = self._untransform_layer_name(this_layer)
        else:
            transformed_name = self._transform_layer_name(this_layer)
        assert transformed_name in all_layers, f"{transformed_name=} not in {all_layers=}"
        return getattr(KC, self._attrib[-2:])(all_layers.index(transformed_name), **self._extra_args)

    def _apply_key(self, key):
        if isinstance(key, CustomLayerKey):
            return key(self._transform_layer_name(key._layer))
        return LAYER_TRANSFORMERS[self._suffix].get(key, self._default_kc)

    def transform_layer(self, layer_name, layer):
        layer = [self._apply_key(k) for k in layer]
        out_name = self._transform_layer_name(layer_name)
        return out_name, layer

    def layer_created(self, *, this_layer, **kwargs):
        if self._attrib.startswith('U'):
            return set()
        return self._transform_layer_name(this_layer)

class FlipTransformLayerKey(CustomKey):
    SUPPORTED = {'FMO'}

    def __init__(self, attrib):
        self._attrib = attrib

    def layer_created(self, *, this_layer, **kwargs):
        if this_layer.endswith('_flip'):
            return this_layer[:-5]
        return f'{this_layer}_flip'

    def transform_layer(self, layer_name, layer):
        rv = [None] * (5 * 12)
        def orig_to_new(n):
            x = n%12
            y = n // 12
            rv = y * 12 + (12 - x) - 1
            return rv
        for i, k in enumerate(layer):
            rv[orig_to_new(i)] = k
        return self.layer_created(this_layer=layer_name), rv

    def code(self, *, all_layers, this_layer, **kwargs):
        new_layer = self.layer_created(this_layer=this_layer)
        assert new_layer in all_layers, f'{new_layer=} not in {all_layers}'
        return getattr(KC, self._attrib[-2:])(all_layers.index(new_layer))


class KeyGetter:
    def __init__(self, *custom_key_classes):
        self.custom_key_classes = custom_key_classes
        self.key_lookup = dict()
        for c in self.custom_key_classes:
            duplicated = set(c.SUPPORTED) & set(self.key_lookup)
            if duplicated:
                raise ValueError(
                    f'duplicate definitions found in {c.__name__}'
                    + ', '.join(map(lambda x: f"{x} defined in {self.key_lookup[x].__NAME__}")))
            for supported in c.SUPPORTED:
                self.key_lookup[supported] = c(supported)

    def __getattr__(self, v):
        if v in self.key_lookup:
            return self.key_lookup[v]
        return getattr(KC, v)

split = Split(
    split_flip=True,  # If both halves are the same, but flipped, set this True
    split_type=SplitType.UART,  # Defaults to UART
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=board.RX,  # The primary data pin to talk to the secondary device with
    data_pin2=board.TX,  # Second uart pin to allow 2 way communication
    use_pio=True,  # allows for UART to be used with PIO
    split_side=configuration.side,
)
keyboard.modules = [_Layers(),  split]

CK = KeyGetter(CustomLayerKey, MapTransformLayerKey, FlipTransformLayerKey)
if configuration.pimoroni:
    def get_color(layer):
        r, g, b, w = 0, 0, 0, 0
        if layer.startswith('qwerty'):
            r += 127
        elif layer.startswith('dvorak'):
            g += 127
        elif layer.startswith('symbols'):
            w += 127
        if 'vim' in layer:
            b += 127
        if 'flip' in layer:
            r += 127
            g += 127
            w += 80
        return r, g, b, w
    from kmk.modules.pimoroni_trackball import Trackball, TrackballMode, PointingHandler, KeyHandler, ScrollHandler, ScrollDirection
    print('detected left side')
    i2c = io.I2C(scl=board.D3, sda=board.D2)
    trackball = Trackball(i2c, mode=TrackballMode.MOUSE_MODE,
        angle_offset=math.radians(-90), handlers=[PointingHandler()])

    keyboard.modules.append(trackball)
    class Layers(_Layers):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            trackball.set_rgbw(0, 0, 0, 0)
            self.last_layer = 0
        def after_hid_send(self, keyboard):
            if keyboard.active_layers[0] != self.last_layer:
                if keyboard.debug_enabled:
                    print('layer swap from',
                          keyboard.layernames[self.last_layer],
                          'to', keyboard.layernames[keyboard.active_layers[0]])
                self.last_layer = keyboard.active_layers[0]
                newname = keyboard.layernames[self.last_layer]
                new_colors = get_color(newname)
                if keyboard.debug_enabled:
                    print('setting colors to', new_colors, keyboard.layernames[self.last_layer])
                trackball.set_rgbw(*new_colors)
    keyboard.modules[0] = Layers()

def populate_layer_transformers():
    return dict(
        vim={
            KC.A: KC.NO, # simple_key_sequence((KC.TG("disable current layer"), KC.END))
            KC.B: KC.LCTL(KC.LEFT),
            KC.C: KC.NO,  # = cut and disable current layer
            KC.D: KC.LCTL(KC.X),  # cut
            KC.E: KC.NO,  # = same as w?
            KC.F: KC.NO,  # don't think its possible
            KC.G: KC.NO,  # nope
            KC.H: KC.NO,  #
            KC.H: KC.LEFT,
            KC.I: CK.UMTG('vim'),  # = disable current layer
            KC.J: KC.DOWN,
            KC.K: KC.UP,
            KC.L: KC.RIGHT,
            KC.M: KC.NO,  # not possible
            KC.N: simple_key_sequence((KC.LCTL(KC.F), KC.ENT)),
            KC.O: simple_key_sequence((KC.END, KC.ENT)),
            KC.P: KC.LCTL(KC.V),  # paste
            KC.Q: KC.NO,  # should be able to record dynamic key sequence (along with the count before replaying)
            KC.R: KC.LCTL(KC.Y),
            KC.S: KC.NO,  #
            KC.T: KC.NO,  #
            KC.U: KC.LCTL(KC.Z),
            KC.V: KC.NO,  # hold shift
            KC.W: KC.LCTL(KC.RIGHT),
            KC.X: KC.DEL,  # delete
            KC.Y: KC.LCTL(KC.C),  # copy
            KC.Z: KC.NO,  # is leader
            KC.SLSH: KC.LCTL(KC.F),
            KC.TRNS: KC.TRNS,
        })
LAYER_TRANSFORMERS = populate_layer_transformers()

# Cleaner key names
SYMB = CK.MO("symbols")
QWERT_S = CK.TG("qwerty")
DVORAK = CK.MO("dvorak")
DVORA_S = CK.TG("dvorak")
RESET = CK.TO("base")
VIM_H = CK.MMO("vim")
VIM_M = CK.MTG("vim")


qwerty_dvorak = {
    KC.A: KC.A, KC.S: KC.O, KC.D: KC.E, KC.F: KC.U, KC.Q: KC.QUOT, KC.MINS: KC.RBRC,
    KC.T: KC.Y, KC.X: KC.Q, KC.C: KC.J, KC.V: KC.K, KC.W: KC.COMM, KC.LBRC: KC.SLSH,
    KC.U: KC.G, KC.I: KC.C, KC.O: KC.R, KC.P: KC.L, KC.Z: KC.SCLN, KC.QUOT: KC.MINS,
    KC.K: KC.T, KC.L: KC.N, KC.N: KC.B, KC.M: KC.M, KC.SCLN: KC.S, KC.DOT: KC.V,
    KC.Y: KC.F, KC.J: KC.H, KC.G: KC.I, KC.B: KC.X, KC.COMM: KC.W, KC.RBRC: KC.EQL,
    KC.H: KC.D, KC.R: KC.P, KC.E: KC.DOT,           KC.SLSH: KC.Z, KC.EQL: KC.RBRC,
}

base = [
    KC.TAB,  QWERT_S, KC.NO,   KC.NO,   KC.NO,   KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.BSPC,
    KC.ESC,  KC.NO,   KC.NO,   DVORA_S, KC.NO,   KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.ENT,
    KC.LSFT, KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.RSFT,
    KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.LALT, KC.NO,       KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.NO,   KC.DEL,
    KC.LGUI, KC.NO,   KC.LCTL, SYMB,    KC.LSFT,  KC.TRNS,     KC.TRNS, KC.SPC,  SYMB,    KC.RCTL, KC.RALT, KC.RGUI,
]

# qwerty
qwerty = [
    KC.TRNS, KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,        KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.TRNS,
    KC.TRNS, KC.A,    KC.S,    KC.D,    KC.F,    KC.G,        KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN, KC.TRNS,
    KC.TRNS, KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,        KC.N,    KC.M,    KC.COMM, KC.DOT,  KC.SLSH, KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    KC.TRNS, VIM_H,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, VIM_M,  KC.TRNS,
]

# dvorak
dvorak = [
    KC.TRNS, KC.QUOT, KC.COMM, KC.DOT,  KC.P,    KC.Y,        KC.F,    KC.G,    KC.C,    KC.R,    KC.L,    KC.TRNS,
    KC.TRNS, KC.A,    KC.O,    KC.E,    KC.U,    KC.I,        KC.D,    KC.H,    KC.T,    KC.N,    KC.S,    KC.TRNS,
    KC.TRNS, KC.SCLN, KC.Q,    KC.J,    KC.K,    KC.X,        KC.B,    KC.M,    KC.W,    KC.V,    KC.Z,    KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, CK.FMO,      CK.FMO,  KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    KC.TRNS, VIM_M,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, VIM_M,   KC.TRNS,
]

symbols = [
    RESET,   KC.NO,   KC.LPRN, KC.RPRN, KC.SLSH, KC.NO,       KC.NO,   KC.BSLS, KC.GRV,  KC.NO,   KC.NO,   KC.NO,
    KC.TRNS,  KC.NO,   KC.LBRC, KC.RBRC, KC.PIPE, KC.PLUS,     KC.MINS, KC.EQL,  KC.UNDS, KC.NO,   KC.NO,   KC.NO,
    KC.TRNS, KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,       KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.NO,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,     KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
]

def copy(layer):
    return [k for k in layer]

def invert(layer):
    rv = [None] * (5 * 12)
    def orig_to_new(n):
        x = n%12
        y = n // 12
        rv = y * 12 + (12 - x) - 1
        return rv
    for i, k in enumerate(layer):
        rv[orig_to_new(i)] = k
    return rv

def create_keymap(*layouts):
    # creates [layout 1, layout 2, ..., layout 1(reversed), layout 2(reversed), ...]
    rv = []
    layer_order = [l[0] for l in layouts]
    layers = [l[1] for l in layouts]
    print('unmodified layers:', layer_order)

    # add created layers
    added = 1
    while added != 0:
        to_add_names = []
        to_add_layers = []
        for name, layer in zip(layer_order, layers):
            for k in layer:
                if isinstance(k, MapTransformLayerKey) or isinstance(k, FlipTransformLayerKey):
                    created_layer = k.layer_created(this_layer=name)
                    print("    creates:", created_layer)
                    if created_layer not in to_add_names + layer_order:
                        newname, newlayer = k.transform_layer(layer_name=name, layer=layer)
                        if newname not in layer_order:
                            to_add_names.append(newname)
                            to_add_layers.append(newlayer)
        added = len(to_add_names)
        print('adding', added, 'modified layers', to_add_names)
        layer_order += to_add_names
        layers += to_add_layers

    for layer_number, (name, layer) in enumerate(zip(layer_order, layers)):
        to_add = []
        print(f"adding layer #{layer_number} ", end='')
        for i, k in enumerate(layer):
            if isinstance(k, CustomKey):
                to_add.append(k.code(all_layers=layer_order, this_layer=name))
            else:
                to_add.append(k)

            if i%12 == 0:
                print('.', end='')
        print(f" got {len(to_add)} keys on layer number {len(rv)} ({name})")
        rv.append(to_add)

    return rv, layer_order

keyboard.keymap, keyboard.layernames = create_keymap(
    ("base", base),
    ("qwerty", qwerty),
    ("dvorak", dvorak),
    ("symbols", symbols),
)


print('keymap created')

if __name__ == '__main__':

    keyboard.active_layers = [0]
    keyboard.debug_enabled = False
    keyboard.go()
