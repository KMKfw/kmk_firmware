# Encoder

Aumente o volume! Acrescente zoom, volume ou qualquer coisa do gênero ao seu
teclado!

## Habilitando a Extensão

O construtor toma no mínimo três argumentos: uma lista de pinos `pad_a`, uma
lista de pinos `pad_b`, e um `encoder_map`. O `encoder_map` é modelado de acordo
com o teclado e funciona da mesma forma. Ele deve ter tantas teclas qyanto seu
teclado, e usar teclas `KC.NO` para camadas que não exijam ação alguma. O
encoder suporta um modo de velocidade se você deseja fazer algo com edição de
áudio ou vídeo. A direção de incremento/decremento pode ser mudada a fim de
fazer par com a direção que o botão está orientado, atribuindo à flag `is_inverted`.

## Configuração

Eis um exemplo completo no `main.py` do  Atreus62.

Crie suas teclas especiais:

```python
Zoom_in = KC.LCTRL(KC.EQUAL)
Zoom_out = KC.LCTRL(KC.MINUS)
```

Crie o `encoder_map`.

Anatomia de uma tupla de `encoder_map`: `(increment_key, decrement_key, teclas
pressionadas por clique do encoder)`

```python

# create the encoder map, modeled after the keymap
encoder_map = [
    [
        # Only 1 encoder is being used, so only one tuple per layer is required
        # Increment key is volume up, decrement key is volume down, and sends 2
        # key presses for every "click" felt while turning the encoder.
        (KC.VOLU,KC.VOLD,2),
    [
        # only one key press sent per encoder click
        (Zoom_in, Zoom_out,1),
    ],
    [
        # No action keys sent here, the resolution is a dummy number, to be
        # removed in the future.
        (_______,_______,1),#
    ]
]

# create the encoder instance, and pass in a list of pad a pins, a lsit of pad b
# pins, and the encoder map created above
encoder_ext = EncoderHandler([board.D40],[board.D41], encoder_map)

# if desired, you can flip the incrfement/decrement direction of the knob by
# setting the is_inerted flag to True.  If you turn the knob to the right and
# the volume goes down, setting this flag will make it go up.  It's default
# setting is False
encoder_ext.encoders[0].is_inverted = True

# Make sure to add the encoder_ext to the modules list
keyboard.modules = [encoder_ext]
```
