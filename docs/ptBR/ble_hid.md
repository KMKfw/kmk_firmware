# BLE HID

Conexões Bluetooth ajudam a se livrar da maçaroca de fios!

## Circuitpython

Se não estiver usando o KMKPython, você precisará da biblioteca `adafruit_ble`
da Adafruit. Ela pode ser baixada
[aqui](https://github.com/adafruit/Adafruit_CircuitPython_BLE/tree/master/adafruit_ble).
Ela faz parte do [Pacotão Adafruit
CircuitPython](https://github.com/adafruit/Adafruit_CircuitPython_Bundle). Simplesmente
coloque-a na raiz do seu dispositivo circuitpython. Se não tiver certeza, é o
primeiro diretório com `main.py` nele, e deve ser o primeiro que você abre
quando acessa o dispositivo.

## Habilitando BLE

Para habilitar o BLE hid, modifique o `keyboard.go()`. Por padrão, o nome
exibido será o nome do "flash drive", o qual por padrão é CIRCUITPY:

```python
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE)
```

## Mudando o Nome Exibido

Existem duas formas de mudar o nome exibido. O primeiro seria [mudando o nome do
do
drive](https://learn.adafruit.com/welcome-to-circuitpython/the-circuitpy-drive). O
segundo seria mudando `keyboard.go()` assim:

```python
if __name__ == '__main__':
    keyboard.go(hid_type=HIDModes.BLE, ble_name='KMKeyboard')
```
