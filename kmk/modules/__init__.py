from typing import NoReturn

from kmk.kmk_keyboard import KMKKeyboard


class InvalidExtensionEnvironment(Exception):
    pass


class Module:
    '''
    Modules differ from extensions in that they not only can read the state, but
    are allowed to modify the state. The will be loaded on boot, and are not
    allowed to be unloaded as they are required to continue functioning in a
    consistant manner.
    '''

    # The below methods should be implemented by subclasses

    def during_bootup(self, keyboard: KMKKeyboard) -> NoReturn:
        raise NotImplementedError

    def before_matrix_scan(self, keyboard: KMKKeyboard) -> NoReturn:
        '''
        Return value will be injected as an extra matrix update
        '''
        raise NotImplementedError

    def after_matrix_scan(self, keyboard: KMKKeyboard) -> NoReturn:
        '''
        Return value will be replace matrix update if supplied
        '''
        raise NotImplementedError

    def before_hid_send(self, keyboard: KMKKeyboard) -> NoReturn:
        raise NotImplementedError

    def after_hid_send(self, keyboard: KMKKeyboard) -> NoReturn:
        raise NotImplementedError

    def on_powersave_enable(self, keyboard: KMKKeyboard) -> NoReturn:
        raise NotImplementedError

    def on_powersave_disable(self, keyboard: KMKKeyboard) -> NoReturn:
        raise NotImplementedError
