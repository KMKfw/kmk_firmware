try:
    from typing import Optional
except ImportError:
    # we're not in a dev environment, so we don't need to worry about typing
    pass
from micropython import const

from kmk.keys import KC, Key
from kmk.modules import Module


class State:
    LISTENING = const(0)
    DELETING = const(1)
    SENDING = const(2)


class Character:
    '''Helper class for making a left-shifted key identical to a right-shifted key'''

    is_shifted: bool = False

    def __init__(self, key_code: Key, is_shifted: bool) -> None:
        self.is_shifted = is_shifted
        self.key_code = KC.LSHIFT(key_code) if is_shifted else key_code

    def __eq__(self, other: any) -> bool:  # type: ignore
        try:
            return (
                self.key_code.code == other.key_code.code
                and self.is_shifted == other.is_shifted
            )
        except AttributeError:
            return False


class Phrase:
    '''Manages a collection of characters and keeps an index of them so that potential matches can be tracked'''

    def __init__(self, string: str) -> None:
        self._characters: list[Character] = []
        self._index: int = 0
        for char in string:
            try:
                key_code = getattr(KC, char.upper())
                shifted = char.isupper() or key_code.has_modifiers == {2}
                self._characters.append(Character(key_code, shifted))
            except ValueError:
                raise ValueError(f'Invalid character in dictionary: {char}')

    def next_character(self) -> None:
        '''Increment the current index for this phrase'''
        if not self.index_at_end():
            self._index += 1

    def get_character_at_index(self, index: int) -> Character:
        '''Returns the character at the given index'''
        return self._characters[index]

    def get_character_at_current_index(self) -> Character:
        '''Returns the character at the current index for this phrase'''
        return self._characters[self._index]

    def reset_index(self) -> None:
        '''Reset the index to the start of the phrase'''
        self._index = 0

    def index_at_end(self) -> bool:
        '''Returns True if the index is at the end of the phrase'''
        return self._index == len(self._characters)

    def character_is_at_current_index(self, character) -> bool:
        '''Returns True if the given character is the next character in the phrase'''
        return self.get_character_at_current_index() == character


class Rule:
    '''Represents the relationship between a phrase to be substituted and its substitution'''

    def __init__(self, to_substitute: Phrase, substitution: Phrase) -> None:
        self.to_substitute: Phrase = to_substitute
        self.substitution: Phrase = substitution

    def restart(self) -> None:
        '''Resets this rule's to_substitute and substitution phrases'''
        self.to_substitute.reset_index()
        self.substitution.reset_index()


class TextReplacement(Module):
    _shifted: bool = False
    _rules: list = []
    _state: State = State.LISTENING
    _matched_rule: Optional[Phrase] = None

    def __init__(
        self,
        dictionary: dict,
    ):
        for entry in dictionary:
            self._rules.append(Rule(Phrase(entry), Phrase(dictionary[entry])))

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not self._state == State.LISTENING:
            return
        if key is KC.LSFT or key is KC.RSFT:
            if is_pressed:
                self._shifted = True
            else:
                self._shifted = False
        if is_pressed:
            character = Character(key, self._shifted)

            # run through the dictionary to check for a possible match on each new keypress
            for rule in self._rules:
                if rule.to_substitute.character_is_at_current_index(character):
                    rule.to_substitute.next_character()
                else:
                    rule.restart()
                    # if character is not a match at the current index,
                    # it could still be a match at the start of the sequence
                    # so redo the check after resetting the sequence
                    if rule.to_substitute.character_is_at_current_index(character):
                        rule.to_substitute.next_character()
                # we've matched all of the characters in a phrase to be substituted
                if rule.to_substitute.index_at_end():
                    rule.restart()
                    # set the phrase indexes to where they differ
                    # so that only the characters that differ are replaced
                    for character in rule.to_substitute._characters:
                        if (
                            character
                            == rule.substitution.get_character_at_current_index()
                        ):
                            rule.to_substitute.next_character()
                            rule.substitution.next_character()
                        else:
                            break
                        if rule.to_substitute.index_at_end():
                            break
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
            to_substitute: Phrase = self._matched_rule.to_substitute  # type: ignore
            to_substitute.next_character()
            if not to_substitute.index_at_end():
                keyboard.tap_key(KC.BSPC)
            else:
                self._state = State.SENDING
                # force-release modifiers so sending the replacement text doesn't interact with them
                # it should not be possible for any modifiers other than shift to be held upon rule activation
                # as a modified key won't send a keycode that is matched against the user's dictionary,
                # but, just in case, we'll release those too
                keys_to_release = [
                    KC.LSHIFT,
                    KC.RSHIFT,
                    KC.LCTL,
                    KC.RCTL,
                    KC.LALT,
                    KC.RALT,
                ]
                for key in keys_to_release:
                    keyboard.remove_key(key)

        if self._state == State.SENDING:
            substitution = self._matched_rule.substitution  # type: ignore
            if not substitution.index_at_end():
                keyboard.tap_key(substitution.get_character_at_current_index().key_code)
                substitution.next_character()
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
