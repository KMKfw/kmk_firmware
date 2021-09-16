# Micro-Controladores Oficialmente Suportados

Enquanto a maioria dos dispositivos com Circuitpython são muito bons para
teclados artesanais, amaioria dos teclados é projetada para aceitar um Pro
Micro. As placas listadas abaixo ou são, ou podem ser adaptadas para essa
pinagem a fim de usar teclados comuns já presentes no mercado.

## Nice!Nano

Características:
- Pinagem Pro Micro
- Suporte a USB HID e Bluetooth
- Pode ser usado para teclados repartidos sem fio (Bluetooth)
- Suporte a bateria, incluindo carga

Desvantagens:
- 25 dólares por micro-controladores na maioria das revendedoras

Varejistas comund:
- [Boardsource](https://boardsource.xyz/store/5f4a1733bbaa5c635b83ed67)
- [NiceKeyboards](https://nicekeyboards.com/collections/group-buy/products/nice-nano-v1-0).

## ItsyBitsy M4 Express

Características:
- Preços acessíveis a partir de 15 dólares
- Pode rodar a maior parte das vantagens do KMK, incluindo RGB

Desvantagens:
- Precisa de adaptadir para funcionar com a pinagem do Pro Micro. O adaptador
  pode ser encontrado
  [AQUI](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)

Varejistas Comuns:
- [Adafruit](https://www.adafruit.com/product/3800)

## RP2040

Características:
- Preço bastante acessível
- Bastante poderosa dado o preço

Desvantagens:
- Pouco suporte para kits de teclado

Varejistas comuns:
- [Adafruit](https://www.adafruit.com/pico?src=raspberrypi)
- [Sparkfun](https://www.sparkfun.com/products/17829?src=raspberrypi)

## Adafruit ItsyBitsy nRF52840 Express

Características:
- Suporte a USB HID e Bluetooth
- Mais acessível que o Nice!Nano, apenas 18 dólares

Desvantagens:
- Precisa de adaptador para funcionar com teclados de pinagem Pro Micro pinout
  keyboards. O adaptador pode ser encontrado
  [AQUI](https://github.com/KMKfw/kmk_firmware/tree/master/hardware)
- O suporte à bateria precisa de uma placa adicional encontrada
  [AQUI](https://www.adafruit.com/product/2124)

Varejistas comuns:
- [Adafruit](https://www.adafruit.com/product/4481)

## Outros Micro-Controladores

O mínimo que você vai precisar:

- CircuitPython/KMKpython
- 256KB de armazenamento flash
- HID sobre USB e/ou Bluetooth.
