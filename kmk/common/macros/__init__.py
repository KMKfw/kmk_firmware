class KMKMacro:
    def __init__(self, keydown=None, keyup=None):
        self.keydown = keydown
        self.keyup = keyup

    def on_keydown(self):
        return self.keydown() if self.keydown else None

    def on_keyup(self):
        return self.keyup() if self.keyup else None
