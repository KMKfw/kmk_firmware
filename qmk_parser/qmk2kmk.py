#!/usr/bin/python
import sys
import json

class Atreus62:
    # A class should be created for each matrix type

    # this layout follows the physical wiring of the matrix.
    # this was a hand wired build for me, so the actual wiring may differ from
    # from other tutorials online

    # there is an extra row to accomodate the thumb keys, this can also  be used
    # for encoder buttons wired into matrix.  This layout gives my drop in 
    # success for converting qmk configurator keymap for atreus62.  It will 
    # require thought, but this should be capable for all other keymaps 
    # provided that you know the wiring of the matrix 
    rows = 6
    cols = 12
    matrix = [
        0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10,  11,
        12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
        36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 
        48, 49, 50, 51, 52, 53, 56, 57, 58, 59, 60, 61,
        -1, -1, -1, -1, -1, 54, 55 , -1,-1, -1, -1, -1
    ]


class Translator:
    
    debug = False
    keymap = [] 
    # this was a quick and dirty lookup dict that fit my purpouse for the 
    # atreus62.  Please expand for your needs
    key_lookup = {
        'KC_1'    : 'KC.N1',
        'KC_2'    : 'KC.N2',
        'KC_3'    : 'KC.N3',
        'KC_4'    : 'KC.N4',
        'KC_5'    : 'KC.N5',
        'KC_6'    : 'KC.N6',
        'KC_7'    : 'KC.N7',
        'KC_8'    : 'KC.N8',
        'KC_9'    : 'KC.N9',
        'KC_0'    : 'KC.N0',
        'KC_A'    : 'KC.A',
        'KC_B'    : 'KC.B',
        'KC_C'    : 'KC.C',
        'KC_D'    : 'KC.D',
        'KC_E'    : 'KC.E',
        'KC_F'    : 'KC.F',
        'KC_G'    : 'KC.G',
        'KC_H'    : 'KC.H',
        'KC_I'    : 'KC.I',
        'KC_J'    : 'KC.J',
        'KC_K'    : 'KC.K',
        'KC_L'    : 'KC.L',
        'KC_M'    : 'KC.M',
        'KC_N'    : 'KC.N',
        'KC_O'    : 'KC.O',
        'KC_P'    : 'KC.P',
        'KC_Q'    : 'KC.Q',
        'KC_R'    : 'KC.R',
        'KC_S'    : 'KC.S',
        'KC_T'    : 'KC.T',
        'KC_U'    : 'KC.U',
        'KC_V'    : 'KC.V',
        'KC_W'    : 'KC.W',
        'KC_X'    : 'KC.X',
        'KC_Y'    : 'KC.Y',
        'KC_Z'    : 'KC.Z',
        'KC_NO'   : 'KC.NO',
        'KC_TRNS' : 'KC.TRNS',
        'KC_TILD' : 'KC.TILD',
        'KC_COMM' : 'KC.COMM',
        'KC_DOT'  : 'KC.DOT',
        'KC_SLSH' : 'KC.SLSH',
        'KC_LBRC' : 'KC.LBRC',
        'KC_LCTL' : 'KC.LCTL',
        'KC_LGUI' : 'KC.LGUI',
        'KC_LALT' : 'KC.LALT',
        'KC_LSFT' : 'KC.LALT',
        'KC_RBRC' : 'KC.LBRC',
        'KC_RCTL' : 'KC.LCTL',
        'KC_RGUI' : 'KC.LGUI',
        'KC_RALT' : 'KC.LALT',
        'KC_RSFT' : 'KC.LALT',
        'KC_GRV'  : 'KC.GRV',
        'KC_BSPC' : 'KC.BSPC',
        'KC_DEL'  : 'KC.DEL',
        'KC_ENT'  : 'KC.ENT',
        'KC_SPC'  : 'KC.SPC',
        'KC_EQL'  : 'KC.EQL',
        'KC_MINS' : 'KC.MINS',
        'KC_QUOT' : 'KC.QUOT',
        'KC_RGUI' : 'KC.RGUI',
        'KC_LPRN' : 'KC.LPRN',
        'KC_RPRN' : 'KC.RPRN',
        'KC_LCBR' : 'KC.LCBR',
        'KC_RCBR' : 'KC.RCBR',
        'KC_TAB'  : 'KC.TAB',
        'KC_UP'   : 'KC.UP',
        'KC_DOWN' : 'KC.DOWN',
        'KC_LEFT' : 'KC.LEFT',
        'KC_RIGHT': 'KC.RIGHT',
        'KC_UNDS' : 'KC.UNDS',
        'KC_PSLS' : 'KC.PSLS',
        'KC_PAST' : 'KC.PAST',
        'KC_PPLS' : 'KC.PPLS',
        'KC_EQUAL': 'KC.EQUAL',
        'KC_ESC'  : 'KC.ESC',
        'KC_BSLS' : 'KC.BSLS',
        'KC_SCLN' : 'KC.SCLN',
        'KC_RGHT' : 'KC.RGHT',
        'KC_PGDN' : 'KC.PGDN',
        'MO(0)'   : 'KC.MO(0)',
        'MO(1)'   : 'KC.MO(1)',
        'MO(2)'   : 'KC.MO(2)',
        'MO(3)'   : 'KC.MO(3)',
        'MO(4)'   : 'KC.MO(4)',
        'MO(5)'   : 'KC.MO(5)',
        'TO(0)'   : 'KC.TO(0)',
        'TO(1)'   : 'KC.TO(1)',
        'TO(2)'   : 'KC.TO(2)',
        'TO(3)'   : 'KC.TO(3)',
        'TO(4)'   : 'KC.TO(4)',
        'TO(5)'   : 'KC.TO(5)',
        'KC_F1'   : 'KC.F1',
        'KC_F2'   : 'KC.F2',
        'KC_F3'   : 'KC.F3',
        'KC_F4'   : 'KC.F4',
        'KC_F5'   : 'KC.F5',
        'KC_F6'   : 'KC.F6',
        'KC_F7'   : 'KC.F7',
        'KC_F8'   : 'KC.F8',
        'KC_F9'   : 'KC.F9',
        'KC_F10'  : 'KC.F10',
        'KC_F11'  : 'KC.F11',
        'KC_F12'  : 'KC.F12',
        'KC_F13'  : 'KC.F13',
        'RESET'   : 'KC.RESET',
    }

    def __init__(self, qmk_file, keyboard, debug=False):
        self.qmk_file = qmk_file
        self.keyboard = keyboard
        self.debug = debug

    def parse(self):
        # read in info.json form qmk configurator download
        with open(self.qmk_file,'r') as f:
            # store json info in a dict
            data = json.load(f)
            # iterate through keymap layers
            for layer in range(len(data['layers'])):
                layer_list = []
                 # for each layer, convert the key from qmk to kmk
                for idx,key in enumerate(self.keyboard.matrix):
                    if key == -1:
                        # this lets us fill in our matrix if it is larger than 
                        # the map read in from qmk, fills holes with KC.NO
                        layer_list.append('XXXXXXX')
                    else:
                        # where ther is a valid index in the json, put it in the
                        # correct place in the kmk keymap
                        layer_list.append(
                            self.key_lookup[data['layers'][layer][key]]
                            )
                # add the layer to our new list of layers
                self.keymap.append(layer_list)
        # produce a kmk keymap that can be pasted into our main.py
        self.translate()
        if self.debug:
            print(self.keymap)

    # this just prints out the new keymap in a format that can be pasted into 
    # our main.py.  the final product isnt pretty yet, but usable
    def translate(self):
        line = ''
        count = 0
        print('keyboard.keymap = [')
        for layer in self.keymap:
            print('\t[')
            for idx,key in enumerate(layer):
                if count <= self.keyboard.cols - 1:
                    line += f'{key},'
                    count += 1
                if count > self.keyboard.cols - 1:
                    print(f'\t\t{line}')
                    line = ''
                    count = 0
            print('\t],')
        print(']')

# usage - path to json file as the only argument
if __name__ == '__main__':
    translator = Translator(sys.argv[1], Atreus62()).parse()
