def process(self, state, action):
    self.logger.warning(action['keycode'])
    if action['keycode'].code == 1000:
        reset(self)
    elif action['keycode'].code == 1050:
        df(self, "Filler", action)


def reset(self):
    self.logger.debug('Rebooting to bootloader')
    import machine
    machine.bootloader()
    return self


def df(self, layer, action):
    """Switches the default layer"""
    self.logger.warning(action['active_layers'])


def mo(layer):
    """Momentarily activates layer, switches off when you let go"""


def lm(layer, mod):
    """As MO(layer) but with mod active"""


def lt(layer, kc):
    """Momentarily activates layer if held, sends kc if tapped"""


def tg(layer):
    """Toggles the layer (enables it if no active, and vise versa)"""


def to(layer):
    """Activates layer and deactivates all other layers"""


def tt(layer):
    """Momentarily activates layer if held, toggles it if tapped repeatedly"""
