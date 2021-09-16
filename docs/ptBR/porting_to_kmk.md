# Portar para o KMK

Portar uma placa para o KMK é bastante simples, e segue o seguinte formato-base:

```python
import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.matrix import DiodeOrientation
{EXTENSIONS_IMPORT}

class KMKKeyboard(_KMKKeyboard):
{REQUIRED}
    extensions = []

```

## REQUERIDO

Isto é projetado para ser substituído com os pinos de definição de seu teclado.
Linhas, colunas e direção dos diodos (se houver) devem ser definidas dessa
forma:

```python
    row_pins = [board.p0_31, board.p0_29, board.p0_02, board.p1_15]
    col_pins = [board.p0_22, board.p0_24, board.p1_00, board.p0_11, board.p1_04]
    diode_orientation = DiodeOrientation.COL2ROW
```

## Pinos Adicionais para Extensões

KMK inclui extensões embutidas para RGB e teclados repartidos, e para economia
de energia. Se estes são aplicáveis ao seu teclado/micro-controlador, os pinos
devem ser acrescentados aqui. Remeta às instruções na respectiva página de
extensões sobre como adicioná-los. Se não pretende adicionar extensões, mantenha
a lista vazia como mostrado.

# Mapeamento Coordenado

Se seu teclado não é eletricamente construído como um quadrado (apesar que a
maioria é), você pode fornecer o mapeamento diretamente. Um exemplo disso é o
teclado [Corne](https://github.com/foostan/crkbd). Ele tem 12 colunas para 3
linhas, e 6 colunas para a linha inferior. Teclados repartidos são contados pelo
total, não por parte separada. Isto seria mais ou menos assim:

```python
from kmk.matrix import intify_coordinate as ic

    coord_mapping = []
    coord_mapping.extend(ic(0, x) for x in range(12))
    coord_mapping.extend(ic(1, x) for x in range(12))
    coord_mapping.extend(ic(2, x) for x in range(12))
    # And now, to handle R3, which at this point is down to just six keys
    coord_mapping.extend(ic(3, x) for x in range(3, 9))
```

## Keymaps

Mapas de teclas (*keymap*) são organizados com listas de listas. Keycodes são
adicionados para cada tecla de cada camada. Veja [keycodes](keycodes.md) para
mais detalhes sobre que keycodes estão disponíveis. Se usar camadas ou outras
extensões, remeta também à página de extensões para keycodes adicionais.

```python
from kb import KMKKeyboard
from kmk.keys import KC

keyboard = KMKKeyboard()

keyboard.keymap = [
    [KC.A, KC.B],
    [KC.C, KC.D],
]

if __name__ == '__main__':
    keyboard.go()
```

## Mais Informação

Mais informação pode ser vista [aqui](config_and_keymap.md)
