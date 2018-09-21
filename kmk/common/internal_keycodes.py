def process(self, state, key):
    self.logger.warning(key)
    if key.code == 1000:
        reset(self)


def reset(self):
    self.logger.debug('Rebooting to bootloader')
    import machine
    machine.bootloader()
    return self
