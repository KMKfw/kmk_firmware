class InvalidExtensionEnvironment(Exception):
    pass


class Extension:
    _enabled = True

    def enable(self, keyboard):
        self._enabled = True

        self.on_runtime_enable(self, keyboard)

    def disable(self, keyboard):
        self._enabled = False

        self.on_runtime_disable(self, keyboard)

    # The below methods should be implemented by subclasses

    def on_runtime_enable(self, keyboard):
        pass

    def on_runtime_disable(self, keyboard):
        pass

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        '''
        Return value will be injected as an extra matrix update
        '''
        pass

    def after_matrix_scan(self, keyboard, matrix_update):
        pass

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass
