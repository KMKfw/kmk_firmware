from kmk.kmk_keyboard import KMKKeyboard


class InvalidExtensionEnvironment(Exception):
    pass


class Extension:
    _enabled = True  # type: bool

    def enable(self, keyboard):
        # type: (KMKKeyboard) -> None
        self._enabled = True

        self.on_runtime_enable(keyboard)

    def disable(self, keyboard):
        # type (KMKKeyboard) -> None
        self._enabled = False

        self.on_runtime_disable(keyboard)

    # The below methods should be implemented by subclasses

    def on_runtime_enable(self, keyboard):
        # type: (KMKKeyboard) -> None
        raise NotImplementedError

    def on_runtime_disable(self, keyboard):
        # type: (KMKKeyboard) -> None
        raise NotImplementedError

    def during_bootup(self, keyboard):
        # type: (KMKKeyboard) -> None
        raise NotImplementedError

    def before_matrix_scan(self, keyboard):
        # type: (KMKKeyboard) -> None
        '''
        Return value will be injected as an extra matrix update
        '''
        raise NotImplementedError

    def after_matrix_scan(self, keyboard):
        # type: (KMKKeyboard) -> None
        '''
        Return value will be replace matrix update if supplied
        '''
        raise NotImplementedError

    def before_hid_send(self, keyboard):
        # type: (KMKKeyboard) -> None
        raise NotImplementedError

    def after_hid_send(self, keyboard):
        # type: (KMKKeyboard) -> None
        raise NotImplementedError

    def on_powersave_enable(self, keyboard):
        # type: (KMKKeyboard) -> None
        raise NotImplementedError

    def on_powersave_disable(self, keyboard):
        # type: (KMKKeyboard) -> None
        raise NotImplementedError
