# RGB/Underglow/Neopixel

Quer um teclado brilhante? Coloque alguma luz nele!

## CircuitPython

Se não estiver usando KMKpython, isto vai exigir a biblioteca neopixel da
Adafruit. Ela pode ser baixada
[aqui](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/6e35cd2b40575a20e2904b096508325cef4a71d3/neopixel.py).
É parte do [Pacotão Adafruit
CircuitPython](https://github.com/adafruit/Adafruit_CircuitPython_Bundle). Coloque-o
na raiz do seu dispositivo circuitpython. Se não souber qual é, é o diretório
com `main.py` nele, e deve ser o primeiro diretório que você vê ao abrir o dispositivo.

Atualmente suportamos os LEDs endereçáveis a seguir:

 * WS2811, WS2812, WS2812B, WS2812C, etc.
 * SK6812, SK6812MINI, SK6805

### Seleção de Cores

KMK usa o sistema
[Hue-Saturation-Value](https://en.wikipedia.org/wiki/HSL_and_HSV) para
selecionar as cores, em vez do RGB. A roda de cores abaixo demonstra seu
funcionamento.

- Mudar o **Hue** dá a volta no círculo.
- Mudar o **Saturation** move entre as seções internas e externas do círculo,
afetando a intensidade da cor.
- Mudar o **Value** atribui o valor do brilho total.

## Habilitando a Extensão

Os únicos valores exigidos para a extensão RGB devem ser o pino de pixel e o
número de pixels/LEDs. Se estiver usando um teclado repartido, este número é por
parte, não pelo total das duas.

```python
from kmk.extensions.RGB import RGB
from kb import rgb_pixel_pin  # This can be imported or defined manually

rgb_ext = RGB(pixel_pin=rgb_pixel_pin, num_pixels=27)
keyboard.extensions.append(rgb_ext)
```

## [Keycodes]

| Key                           | Aliases    | Descrição                               |
|-------------------------------|------------|-----------------------------------------|
| `KC.RGB_TOG`                  |            | Liga/desliga o RGB                      |
| `KC.RGB_HUI`                  |            | Aumenta Hue                             |
| `KC.RGB_HUD`                  |            | Diminui Hue                             |
| `KC.RGB_SAI`                  |            | Aumenta Saturation                      |
| `KC.RGB_SAD`                  |            | Diminui Saturation                      |
| `KC.RGB_VAI`                  |            | Aumenta Value                           |
| `KC.RGB_VAD`                  |            | Diminui Value                           |
| `KC.RGB_ANI`                  |            | Aumenta a velocidade da animação        |
| `KC.RGB_AND`                  |            | Diminui a velocidade da animação        |
| `KC.RGB_MODE_PLAIN`           | `RGB_M_P`  | RGB Estático                            |
| `KC.RGB_MODE_BREATHE`         | `RGB_M_B`  | Animação de Respiração                  |
| `KC.RGB_MODE_RAINBOW`         | `RGB_M_R`  | Animação de Arco-Íris                   |
| `KC.RGB_MODE_BREATHE_RAINBOW` | `RGB_M_BR` | Animação de Arco-Íris Respirando        |
| `KC.RGB_MODE_KNIGHT`          | `RGB_M_K`  | Animação de SuperMáquina (Knight Rider) |
| `KC.RGB_MODE_SWIRL`           | `RGB_M_S`  | Animação de Redemoinho                  |

## Configuração

| Definição                            | Padrão      | Descrição                                                             |
|--------------------------------------|-------------|-----------------------------------------------------------------------|
| `keyboard.pixel_pin`                 |             | O pino conectado ao pino de dados dos LEDs                            |
| `keyboard.num_pixels`                |             | O número de LEDs conectados                                           |
| `keyboard.rgb_config['rgb_order']`   | `(1, 0, 2)` | A ordem dos pixels RGB, e opcionalmente branco. Exemplo: (1, 0, 2, 3) |
| `keyboard.rgb_config['hue_step']`    | `10`        | O número de passos para ciclar ao longo do Hue                        |
| `keyboard.rgb_config['sat_step']`    | `17`        | O número de passos para mudar a Saturation                            |
| `keyboard.rgb_config['val_step']`    | `17`        | O número de passos para mudar o Value (brilho)                        |
| `keyboard.rgb_config['hue_default']` | `0`         | Hue padrão quando o teclado inicia                                    |
| `keyboard.rgb_config['sat_default']` | `100`       | Saturation padrão quando o teclado inicia                             |
| `keyboard.rgb_config['val_default']` | `100`       | Value padrão (brilho) quando o teclado inicia                         |
| `keyboard.rgb_config['val_limit']`   | `255`       | Nível máximo de brilho                                                |

## Configuração da Animação Embutida

| Definição                                     | Padrão | Descrição                                                                                     |
|-----------------------------------------------|--------|-----------------------------------------------------------------------------------------------|
| `keyboard.rgb_config['breathe_center']`       | `1.5`  | Usado para calcular a curva da animação de respiração. Qualquer valor em 1.0-2.7 é válido. |
| `keyboard.rgb_config['knight_effect_length']` | `4`    | O número de LEDs a ligar para a animação do KITT (SuperMáquina)                               |

## Funções

Se você quer criar suas próprias animações, ou por exemplo mudar a luminosidade
numa macro, ou numa troca de camadas, eis  algumas funções disponíveis:

| Function                                        | Descrição                                                                                                                    |
|-------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `keyboard.pixels.set_hsv_fill(hue, sat, val)`   | Preenche todos os LEDs com valores HSV                                                                                       |
| `keyboard.pixels.set_hsv(hue, sat, val, index)` | Atribui um valor HSV a um LED específico                                                                                     |
| `keyboard.pixels.set_rgb_fill((r, g, b))`       | Preenche todos os LEDs com valores RGB(W)                                                                                    |
| `keyboard.pixels.set_rgb((r, g, b), index)`     | Atribui um valor RGB(W) a um LED específico                                                                                  |
| `keyboard.pixels.disable_auto_write(bool)`      | Quando `True`, desabilita mostrar as mudanças. Bom para atribuir múltiplas mudanças de LEDs antes de uma atualização visível |
| `keyboard.pixels.increase_hue(step)`            | Aumenta Hue de um `step` dado                                                                                                |
| `keyboard.pixels.decrease_hue(step)`            | Diminui Hue de um `step` dado                                                                                                |
| `keyboard.pixels.increase_sat(step)`            | Aumenta Saturation de um `step` dado                                                                                         |
| `keyboard.pixels.decrease_sat(step)`            | Diminui Saturation de um `step` dado                                                                                         |
| `keyboard.pixels.increase_val(step)`            | Aumenta Value (brilho) de um `step` dado                                                                                     |
| `keyboard.pixels.decrease_val(step)`            | Diminui Value (brilho) de um `step` dado                                                                                     |
| `keyboard.pixels.increase_ani()`                | Aumenta a velocidade da animação de 1. Máximo 10                                                                             |
| `keyboard.pixels.decrease_ani()`                | Diminui a velocidade da animação de 1. Mínimo 10                                                                             |
| `keyboard.pixels.off()`                         | Desliga todos os LEDs                                                                                                        |
| `keyboard.pixels.show()`                        | Exibe todas as configurações armazenadas para os LEDs. Útil quando `disable_auto_write` explicado abaixo                     |
| `keyboard.pixels.time_ms()`                     | Retorna um tempo em milissegundos desde que o teclado foi ligado. Útil para temporizadores de início/parada                  |


## Acesso Direto às Variáveis

| Definição                           | Padrão   | Descrição                                                                                                                              |
|-------------------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------|
| `keyboard.pixels.hue`               | `0`      | Atribui à Hue, 0-360                                                                                                                   |
| `keyboard.pixels.sat`               | `100`    | Atribui à Saturation, 0-100                                                                                                            |
| `keyboard.pixels.val`               | `80`     | Atribui ao Brightness, 1-255                                                                                                           |
| `keyboard.pixels.reverse_animation` | `False`  | Se `True`, algumas animações vão rodar ao contrário. Pode ser usado seguramente em animações do usuário                                |
| `keyboard.pixels.animation_mode`    | `static` | Isto pode ser modificado para quaisquer modos inclusos, ou para algo customizado para interações do usuário. Qualquer string é válida. |
| `keyboard.pixels.animation_speed`   | `1`      | Aumenta a velocidade da animação na maior parte das animações. Recomendado 1-5, máximo 10.                                             |

```python
from kmk.extensions.rgb import AnimationModes
rgb_ext = RGB(pixel_pin=rgb_pixel_pin,
        num_pixels=27
        num_pixels=0,
        val_limit=100,
        hue_default=0,
        sat_default=100,
        rgb_order=(1, 0, 2),  # GRB WS2812
        val_default=100,
        hue_step=5,
        sat_step=5,
        val_step=5,
        animation_speed=1,
        breathe_center=1,  # 1.0-2.7
        knight_effect_length=3,
        animation_mode=AnimationModes.STATIC,
        reverse_animation=False,
        )
```

## Modificação do Hardware

Para incluir LEDS em placas que não têm suporte nativo, você terá que
acrescentar três fios. O de força correm nos pinos de 3.3V ou 5V (dependendo do
LED), pinos de terra e dados precisarão ser adicionados a um pino não usado em
seu micro-controlador a não ser que seu teclado tenha pontos de soldagem
específicos para eles. Com estes três fios conectados, atribua ao `pixel_pin`
como descrito acima, e você está pronto para usar seus RGB LED's/Neopixels.

## Consertando os Problemas

### Cores Incorretas

Se as cores estão erradas, confira a ordem dos pixels nos seus LEDs
específicos. Eis alguns comuns.

* WS2811, WS2812, WS2812B, WS2812C são todos GRB (1, 0, 2)
* SK6812, SK6812MINI, SK6805 são todos GRB (1, 0, 2)
* Neopixels variam dependendo de onde você compra. Isto vem informado na página
  do produto.

### Luzes não ligam

Certifique-se de que sua placa suporta luz de fundo de LED, conferindo por uma
linha com `PIXEL_PIN`. Se não tiver, você pode adicionar ao seu keymap. Se você
adicionou os LEDs por conta própria, você também precisa atribuir a `num_pixels`
o número total de LEDs instalados.
