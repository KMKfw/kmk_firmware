'''Adds international keys'''
from kmk.extensions import Extension
from kmk.keys import make_key


class International(Extension):
    '''Adds international keys'''

    def __init__(self):
        # International
        make_key(code=50, names=('NONUS_HASH', 'NUHS'))
        make_key(code=100, names=('NONUS_BSLASH', 'NUBS'))
        make_key(code=101, names=('APP', 'APPLICATION', 'SEL', 'WINMENU'))

        make_key(code=135, names=('INT1', 'RO'))
        make_key(code=136, names=('INT2', 'KANA'))
        make_key(code=137, names=('INT3', 'JYEN'))
        make_key(code=138, names=('INT4', 'HENK'))
        make_key(code=139, names=('INT5', 'MHEN'))
        make_key(code=140, names=('INT6',))
        make_key(code=141, names=('INT7',))
        make_key(code=142, names=('INT8',))
        make_key(code=143, names=('INT9',))
        make_key(code=144, names=('LANG1', 'HAEN'))
        make_key(code=145, names=('LANG2', 'HAEJ'))
        make_key(code=146, names=('LANG3',))
        make_key(code=147, names=('LANG4',))
        make_key(code=148, names=('LANG5',))
        make_key(code=149, names=('LANG6',))
        make_key(code=150, names=('LANG7',))
        make_key(code=151, names=('LANG8',))
        make_key(code=152, names=('LANG9',))

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
