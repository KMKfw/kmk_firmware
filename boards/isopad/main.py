from kb import KMKKeyboard

from kmk.keys import KC

Isopad = KMKKeyboard()

Isopad.keymap = [[KC.ENTER]]

if __name__ == '__main__':
    Isopad.go()
