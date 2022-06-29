from kmk.extensions.lock_status import LockStatus


class Indicator(LockStatus):
    def __init__(self):
        super().__init__()
        self.layers = []

    def after_hid_send(self, sandbox):
        backup = self.report
        super().after_hid_send(sandbox)
        if self.report != backup:
            self.update()

    def after_matrix_scan(self, sandbox):
        if self.layers != sandbox.active_layers:
            self.layers = sandbox.active_layers.copy()
            self.update()

    def update(self):
        raise NotImplementedError
