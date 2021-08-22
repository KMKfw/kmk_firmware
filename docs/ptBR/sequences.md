# Sequências

Sequências são usadas para enviar múltiplos pressionamentos de teclas em uma
única ação, e pode ser usado para coisas como caracteres Unicode (até mesmo
emojis! 🇨🇦), geradores lorei epsum, disparo de efeitos colaterais (pense em
iluminação, apitos, mineradores de criptomoedas otimizados para
micro-controladores, etc.). Se você ainda não tem certeza do que é isso, a
maioria dos fornecedores chama estes de "Macros", mas pode fazer muito mais se
você quiser.

## Enviar Strings

A sequência mais básica é `send_string`. Ela pode ser usada para enviar qualquer
caractere do alfabeto inglês, e um conjunto de outras teclas "padrão" (Enter,
espaço, ponto de exclamação, etc.)

```python
from kmk.handlers.sequences import send_string

WOW = send_string("Wow, KMK is awesome!")

keyboard.keymap = [...WOW,...]
```

## Unicode

Antes de tentar enviar sequências de Unicode, certifique-se que você habilite o
seu `UnicodeMode`. Você pode atribuir um valor inicial no seu keymap pela
variável `keyboard.unicode_mode`.

São fornecidas teclas para mudar este modo em tempo de execução - por exemplo,
`KC.UC_MODE_LINUX`.

### Modos Unicode

No Linux, Unicode usa `Ctrl-Shift-U`, suportado pelo `ibus` e GTK+3. Usuários de
`ibus` precisarão acrescentar `IBUS_ENABLE_CTRL_SHIFT_U=1` aos seus ambientes
(`~/profile`, `~/.bashrc`, `~/.zshrc`, ou o configurador do seu desktop).

No Windows, é necessário usar o
[WinCompose](https://github.com/samhocevar/wincompose).

- Linux : `UnicodeMode.LINUX` ou `UnicodeMode.IBUS`.
- Mac: `UnicodeMode.MACOS` ou `UnicodeMode.OSX` ou `UnicodeMode.RALT`.
- Windows: `UnicodeMode.WINC`.


### Exemplos Unicode

Para enviar um símbolo Unicode:

```python
from kmk.handlers.sequences import unicode_string_sequence

FLIP = unicode_string_sequence('(ノಠ痊ಠ)ノ彡┻━┻')

keyboard.keymap = [...FLIP,...]
```

Se, em vez disso, você manter uma tabela de busca de suas sequências (talvez
para atrelar emojis às teclas), isto também é suportado, mediante um processo
extremamente prolixo:

```python
from kmk.handlers.sequences import compile_unicode_string_sequences as cuss

emoticons = cuss({
    'BEER': r'🍺',
    'HAND_WAVE': r'👋',
})

keymap = [...emoticons.BEER, emoticons.HAND_WAVE...]
```

> Um observador notará que a notação-de-ponto (*dot notation*) é suportada aqui,
> apesar de preencher um dicionário - o retorno de
> `compile_unicode_string_sequences` é um `kmk.types.AttrDict`, que você pode
> entender como uma visão somente-leitura sobre um dicionário acrescentando
> acesso baseado em atributos (*dot notation*).

Finalmente, se você precisa enviar pontos-de-código Unicode em modo bruto, isto
é suportado também, mediante `unicode_codepoint_sequence`.

```python
from kmk.handlers.sequences import unicode_codepoint_sequence

TABLE_FLIP = unicode_codepoint_sequence([
    "28", "30ce", "ca0", "75ca","ca0", "29",
    "30ce", "5f61", "253b", "2501", "253b",
])

keyboard.keymap = [...TABLE_FLIP,...]
```
