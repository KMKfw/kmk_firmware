from kmk.keys import KC
from kmk.modules import Module


class State:
    LISTENING = 0
    DELETING = 1
    SENDING = 2


# this class exists as an easy way to compare keys in a manner where
# a right-shifted key would be equivalent to a left-shifted key
class Character:
    is_shifted = False

    def __init__(self, key_code, is_shifted) -> None:
        self.is_shifted = is_shifted
        self.key_code = KC.LSHIFT(key_code) if is_shifted else key_code

    def __eq__(self, other):
        return (
            self.key_code.code == other.key_code.code
            and self.is_shifted == other.is_shifted
        )


class Phrase:
    def __init__(self, characters) -> None:
        self._characters = characters
        self._index = 0

    def next_character(self):
        character = self._characters[self._index]
        self._index += 1
        return character

    def reset(self):
        self._index = 0

    def index_at_end(self):
        return self._index == len(self._characters)

    def character_is_next(self, character):
        return self._characters[self._index] == character


class Rule:
    def __init__(self, to_substitute, substitution) -> None:
        self.to_substitute = to_substitute
        self.substitution = substitution

    def restart(self):
        self.to_substitute.reset()
        self.substitution.reset()


class TextReplacement(Module):
    _shifted = False
    _rules = []
    _state = State.LISTENING
    _matched_rule = None

    def __init__(
        self,
        dictionary,
    ):
        for entry in dictionary:
            to_substitute = []
            substitution = []
            for char in entry:
                if char == "_":
                    key_code = KC.LSHIFT(KC.MINUS)
                else:
                    key_code = getattr(KC, char.upper())
                shifted = char.isupper() or key_code.has_modifiers == {2}
                to_substitute.append(Character(key_code, shifted))
            for char in dictionary[entry]:
                if char == "_":
                    key_code = KC.LSHIFT(KC.MINUS)
                else:
                    key_code = getattr(KC, char.upper())
                shifted = char.isupper() or key_code.has_modifiers == {2}
                substitution.append(Character(key_code, shifted))
            self._rules.append(Rule(Phrase(to_substitute), Phrase(substitution)))

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not self._state == State.LISTENING:
            return
        if key is KC.LSFT or key is KC.RSFT:
            if is_pressed:
                self._shifted = True
            else:
                self._shifted = False
        elif is_pressed:
            character = Character(key, self._shifted)
            # run through the dictionary to check for a possible match on each new keypress
            for rule in self._rules:
                if rule.to_substitute.character_is_next(character):
                    rule.to_substitute.next_character()
                else:
                    rule.restart()
                    # if character is not a match at the current index,
                    # it could still be a match at the start of the sequence
                    # so redo the check after resetting the sequence
                    if rule.to_substitute.character_is_next(character):
                        rule.to_substitute.next_character()
                # we've matched all of the characters in a phrase to be substituted
                if rule.to_substitute.index_at_end():
                    rule.restart()
                    self._matched_rule = rule
                    self._state = State.DELETING
                    # if we have a match there's no reason to continue the full key processing, so return out
                    return
        return super().process_key(keyboard, key, is_pressed, int_coord)

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):

        if self._state == State.LISTENING:
            return

        if self._state == State.DELETING:
            # send backspace taps equivalent to the length of the phrase to be substituted
            to_substitute = self._matched_rule.to_substitute
            to_substitute.next_character()
            if not to_substitute.index_at_end():
                keyboard.tap_key(KC.BSPC)
            else:
                self._state = State.SENDING
                # if the user is holding shift, force-release it so that it doesn't modify the string to be sent
                keyboard.remove_key(KC.LSFT)
                keyboard.remove_key(KC.RSFT)

        if self._state == State.SENDING:
            substitution = self._matched_rule.substitution
            if not substitution.index_at_end():
                keyboard.tap_key(substitution.next_character().key_code)
            else:
                self._state = State.LISTENING
                self._matched_rule = None
                for rule in self._rules:
                    rule.restart()

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return
