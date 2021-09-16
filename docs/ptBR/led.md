# LED (Luz de Fundo Monocor)

Quer um teclado brilhante? Coloque algumas luzes!

## Habilitando a Extensão

Os únicos valores exigidos para a extensão LED são o pino de pixel e o número de
pixels/LEDs. Ao usar um teclado repartido, este número é referente a cada lado,
não ao total dos dois juntos.

```python
from kmk.extensions.RGB import RGB
from kb import led_pin  # This can be imported or defined manually

led_ext = LED(led_pin=led_pin)
keyboard.extensions.append(led_ext)
```

## [Keycodes]

| Tecla                 | Alternativa | Descrição                        |
|-----------------------|-------------|----------------------------------|
| `KC.LED_TOG`          |             | Muda o estado dos LEDs           |
| `KC.LED_INC`          |             | Aumenta o brilho                 |
| `KC.LED_DEC`          |             | Diminui o brilho                 |
| `KC.LED_ANI`          |             | Aumenta a velocidade da animação |
| `KC.LED_AND`          |             | Diminui a velocidade da animação |
| `KC.LED_MODE_PLAIN`   | `LED_M_P`   | Led Estático                     |
| `KC.LED_MODE_BREATHE` | `LED_M_B`   | Animação de respiração           |


## Configuração

Todos esses valores podem ser atribuídos por padrão quando o teclado inicia.

```python
from kmk.extensions.led import AnimationModes
led_ext = LED(
    led_pin=led_pin,
    brightness_step=5,
    brightness_limit=100,
    breathe_center=1.5,
    animation_mode=AnimationModes.STATIC,
    animation_speed=1,
    val=100,
    )
```
