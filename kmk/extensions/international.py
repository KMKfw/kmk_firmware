'''Adds international keys'''

from kmk.extensions import Extension
from kmk.keys import KeyboardKey, make_key


class International(Extension):
    '''Adds international keys'''

    def __init__(self):
        # International
        codes = (
            (50, ('NONUS_HASH', 'NUHS')),
            (100, ('NONUS_BSLASH', 'NUBS')),
            (101, ('APP', 'APPLICATION', 'SEL', 'WINMENU')),
            (135, ('INT1', 'RO')),
            (136, ('INT2', 'KANA')),
            (137, ('INT3', 'JYEN')),
            (138, ('INT4', 'HENK')),
            (139, ('INT5', 'MHEN')),
            (140, ('INT6',)),
            (141, ('INT7',)),
            (142, ('INT8',)),
            (143, ('INT9',)),
            (144, ('LANG1', 'HAEN')),
            (145, ('LANG2', 'HAEJ')),
            (146, ('LANG3',)),
            (147, ('LANG4',)),
            (148, ('LANG5',)),
            (149, ('LANG6',)),
            (150, ('LANG7',)),
            (151, ('LANG8',)),
            (152, ('LANG9',)),
        )
        for code, names in codes:
            make_key(names=names, constructor=KeyboardKey, code=code)

    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
