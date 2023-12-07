# Economia de Energia

Este módulo permite economizar energia, e é voltado para teclados bluetooth/com
bateria.

## Keycodes

| Tecla        | Descrição                        |
|--------------|----------------------------------|
| `KC.PS_TOG ` | Muda a economia ligado/desligado |
| `KC.PS_ON `  | Liga a economia                  |
| `KC.PS_OFF ` | Desliga a economia               |

# Habilitando a Extensão

Para ligar a economia básica, isso é tudo o que é preciso:

```python
from kmk.modules.power import Power

power = Power()

keyboard.modules.append(power)

```

## Economia Extra Opcional

Em placas com suporte, como a nice!nano, a energia pode ser cortada no VCC,
economizando energia extra se OLEDs ou RGBs estão instalados. Eles consomem
energia mesmo que estejam desligados, então isto os impede disso.

```python
from kmk.modules.power import Power

# Your kb.py may already have this set. If not, add it like this
# import board
# keyboard.powersave_pin = board.P0_13
power = Power(powersave_pin=keyboard.powersave_pin)

keyboard.modules.append(power)

```

Certifique-se que o pino é o correto para seu micro-controlador. O exemplo dado
foi para o nice!nano. Nem todos os micro-controladores têm esta característica e
ela pode ser omitida se não houver, simplesmente haverá menos economia de
energia.
