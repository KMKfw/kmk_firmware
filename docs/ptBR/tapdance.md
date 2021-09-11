# Tapdance

Tapdance é uma forma de permitir que uma tecla física funcione como teclas/ações
lógicas múltiplas sem usar camadas. Com tapdance básico, você pode disparar
estas macros ou teclas "aninhadas" mediante uma série de toques (*taps*) da
tecla física dentro de um tempo limite dado.

A ação "lógica" resultante funciona como qualquer outra tecla - ela pode ser
pressionada e liberada imediatamente, ou pode ser segurada. Por exemplo, tomemos
a tecla `KC.TD(KC.A, KC.B)`. Se a tecla de tapdance é pressionada e liberada
rapidamente, a letra "a" é enviada. Se é tocada e liberada duas vezes
rapidamente, a letra "b" será enviada. Se é tocada e segurada uma vez, a letra
"a" será segurada até que a tecla de tapdance seja liberada. Se é tocada e
liberada uma vez rapidamente, e daí tocada e segurada (ambas as ações dentro do
tempo limite), a letra "b" será mantida até que a tecla de tapdance seja
liberada.

Para usar isso, você pode desejar definir um valor para `tap_time` na
configuração de seu teclado. Este valor é um inteiro indicando o tempo em
milissegundos, e seu valor padrão é  `300`.

Você pode então desejar criar uma sequência de teclas usando
`KC.TD(KC.SOMETHING, KC.SOMETHING_ELSE, MAYBE_THIS_IS_A_MACRO, WHATEVER_YO)`, e
colocar em algum lugar. Os únicos limites em quantas teclas pode haver numa
sequência são, teoricamente, o montante de memória RAM na sua
microcontroladora/placa, e quão rápido você pode pressionar a tecla física. Eis
a sua chance de usar toda sua experiência de anos e anos estraçalhando o botão
nos videogames.

**NOTE**: Correntemente nossa implementação de tapdance têm algumas limitações,
as quais pretendemos consertar "eventualmente", mas por ora é bom notar:

- O comportamento de troca momentânea de camadas em uma sequência de tapdance é
  atualmente "indefinido" na melhor hipótese, e provavelmente vai quebrar seu
  teclado. Por ora, recomendamos fortemente evitar `KC.MO`, bem como qualquer
  outra tecla de modificação de camada que use comportamento de troca
  momentânea - `KC.LM`, `KC.LT`, and `KC.TT`.

Eis um exemplo de tudo isso em ação:

```python
from kmk.keycodes import KC
from kmk.macros.simple import send_string

keyboard = KMKKeyboard()

keyboard.tap_time = 750

EXAMPLE_TD = KC.TD(
    KC.A,  # Tap once for "a"
    KC.B,  # Tap twice for "b"
    # Tap three times to send a raw string via macro
    send_string('macros in a tap dance? I think yes'),
    # Tap four times to toggle layer index 1
    KC.TG(1),
)

keyboard.keymap = [[ ...., EXAMPLE_TD, ....], ....]
```
