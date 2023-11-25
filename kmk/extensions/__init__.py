class InvalidExtensionEnvironment(Exception):
    pass


class Extension:
    _enabled = True

    def enable(self, keyboard):
        self._enabled = True

        self.on_runtime_enable(keyboard)

    def disable(self, keyboard):
        self._enabled = False

        self.on_runtime_disable(keyboard)

    # The below methods should be implemented by subclasses

    def on_runtime_enable(self, keyboard):
        raise NotImplementedError

    def on_runtime_disable(self, keyboard):
        raise NotImplementedError

    def during_bootup(self, keyboard):
        raise NotImplementedError

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        raise NotImplementedError

    def after_matrix_scan(self, keyboard):
        '''
        Return value will be replace matrix update if supplied
        '''
        raise NotImplementedError

    def before_hid_send(self, keyboard):
        raise NotImplementedError

    def after_hid_send(self, keyboard):
        raise NotImplementedError

    def on_powersave_enable(self, keyboard):
        raise NotImplementedError

    def on_powersave_disable(self, keyboard):
        raise NotImplementedError

    def deinit(self, keyboard):
        pass
