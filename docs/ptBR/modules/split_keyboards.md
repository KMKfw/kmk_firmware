# Teclados Repartidos

Teclados repartidos são quase a mesma coisa que os inteiriços. UART com fio é
totalmente suportada, e os teclados repartidos com Bluetooth estão em fase de
teste, porém não oferecemos suporte a eles atualmente.

## UART com Fio

Conexões com fio podem usar UART com um ou dois fios. Com dois, você poderá
sincronizar as partes, o que habilita características adicionais em algumas
extensões.

```python
from kb import data_pin
:from kmk.modules.split import Split, SplitType

split = Split(split_side=SplitSide.LEFT)
keyboard.modules.append(split)
```

## Bluetooth (no TRRS) [Atualmente em fase de testes]

Repartidos sem fio são completamente providos de comunicação de via dupla,
permitindo que todas as extensões fuincionem 100%.

```python
from kb import data_pin
from kmk.modules.split import Split, SplitType, Split_Side


split = Split(split_type=Split.BLE, split_side=SplitSide.LEFT)
OR
split = Split(split_type=Split.BLE, split_side=SplitSide.LEFT)
keyboard.modules.append(split)
```

### Configuração

Opções úteis de configuração:

```python
split = Split(
    split_flip=True,  # If both halves are the same, but flipped, set this True
    split_side=None,  # Sets if this is to SplitSide.LEFT or SplitSide.RIGHT, or use EE hands
    split_type=SplitType.UART,  # Defaults to UART
    split_target_left=True,  # If you want the right to be the target, change this to false
    uart_interval=20,  # Sets the uarts delay. Lower numbers draw more power
    data_pin=None,  # The primary data pin to talk to the secondary device with
    data_pin2=None,  # Second uart pin to allow 2 way communication
    target_left=True,  # Assumes that left will be the one on USB. Set to folse if it will be the right
    uart_flip=True,  # Reverses the RX and TX pins if both are provided
)

```

### EE HANDS

Se você quer plugar USB em qualquer dos dois lados, ou usa Bluetooth, esta é
para você.

Renomeie seu drive CIRCUITPY para alguma coisa diferente. O lado esquerdo deve
terminar em L (de *left*) e o direito em R (de *right*). O nome deve ter 11
caracteres ou menos! Esta é uma limitação do sistema de arquivos. (Por exemplo,
NYQUISTL para o lado esquerdo e NYQUISTR para o direito.) Se você escolher um
nome com mais de 11 caracteres, irá receber um erro. Instruções sobre como fazer
isso estão
[aqui](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive).

Para conexões com fio, você não precisa ajustar nada. Para Bluetooth, remova o
`split_side` assim:

```python
# Wired
split = Split()
# Wireless
split = Split(split_type=Split.BLE)
```
