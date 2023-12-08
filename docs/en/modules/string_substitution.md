# String Substitution

The String Substitution module lets a user replace one typed sequence of characters with another. If a string of characters you type matches an entry in your dictionary, it gets deleted and replaced with the corresponding replacement string.

Potential uses:

- Rudimentary auto-correct: replace `yuo` with `you`
- Text expansion, à la [espanso](https://github.com/federico-terzi/espanso): when `:sig` is typed, replace it with `John Doe`, or turn `idk` into `I don't know`

## Usage

The String Substitution module takes a single argument to be passed during initialization: a user-defined dictionary where the keys are the text to be replaced and the values are the replacement text.

Example is as follows:

```python
from kmk.modules.string_substitution import StringSubstitution

my_dictionary = {
    'yuo': 'you',
    ':sig': 'John Doe',
    'idk': "I don't know"
}
string_substitution = StringSubstitution(dictionary=my_dictionary)
keyboard.modules.append(string_substitution)
```

### Recommendations

1. Consider prefixing text expansion entries with a symbol to prevent accidental activation: `:sig`, `!email`, etc.
2. If you want multiple similar replacements, consider adding a number to prevent unreachable matches: `replaceme1`, `replaceme2`, etc.

### Limitations

1. Currently supports characters for which there is a corresponding keycode in KMK - support for international characters is not implemented.
2. Since this runs on your keyboard, it is not context-aware. It can't tell if you are typing in a valid text field or not.
3. In the interest of a responsive typing experience, the first valid match will be used as soon as it is found. If your dictionary contains `abc` and `abcd`, `abcd` will never match.
