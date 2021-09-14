# Começando
> A vida era como uma caixa de chocolates. Você nunca saberia o que iria
> encontrar.

KMK é uma camada focada em teclados que assenta-se em cima de
[CircuitPython](https://circuitpython.org/). Como tal, ela deve funcionar com a
maior parte das [placas que suportam
CircuitPython](https://circuitpython.org/downloads). É melhor usar a última
versão estável (>5.0). Dispositivos funcionais e recomendados podem ser
encontrados [aqui](Officially_Supported_Microcontrollers.md)

Também fornecemos uma versão de CircuitPython otimizada para teclados
(simplificada para lidar com os limites de certas placas e com a seleção dos
módulos relevantes pré-instalados). Se você estiver se perguntando por que usar
KMKPython em vez do CircuitPython cru, tentamos comparar ambas as abordagens
[aqui](kmkpython_vs_circuitpython.md)

<br>

## Guia Rápido
> Ao Infinito e Além!

1. [Installe CircuitPython na tua
   placa](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython).
   Com a maioria das placas, deve ser algo tão fácil quanto copiar e colar o
   firmware no drive.
2. Obtenha uma [cópia do
   KMK](https://github.com/KMKfw/kmk_firmware/archive/refs/heads/master.zip) a
   partir do ramo master.
3. Descompacte e cole o diretório KMK e o arquivo boot.py na raiz do drive USB
   correspondente à tua placa (geralmente aparecendo como CIRCUITPY).
4. Crie um novo arquivo *code.py* ou *main.py* no mesmo diretório raiz (no
   mesmo nível de boot.py) com o exemplo contido abaixo:

***IMPORTANTE:*** adapte os pinos GP0 / GP1 para a tua placa específica! <br>

```
print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.matrix import DiodeOrientation

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP0,)
keyboard.row_pins = (board.GP1,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [KC.A,]
]

if __name__ == '__main__':
    keyboard.go()
```

5. Usando um fio, um clipe de papel ou o que seja, conecte o GPIO 0 e o GPIO 1
   (ou os pinos que você escolheu para tua placa).

6. Se ela imprimir um "A" (ou um "Q" ou o que depender do teu layout de
   teclado), você conseguiu!

<br>


## Agora que tudo está no seu lugar, você pode querer ir além...

> Esta é tua última chance. Após isso Esta é sua última chance. Depois não há
> como voltar. Se tomar a pílula azul a história acaba, e você acordará na sua
> cama acreditando no que quiser. Se tomar a pílula vermelha ficará no País das
> Maravilhas e eu te mostrarei até onde vai a toca do coelho. Lembre-se: tudo o
> que estou te oferecendo é a verdade. Nada mais.

### Você é extremamente sortudo e tem um teclado totalmente suportado

Se seu teclado e micro-controlador são suportados oficialmente, simplesmente
visite a webpage com os seus arquivos e coloque-os na raiz do "flash drive".
Estas webpages podem ser vistas [aqui](https://github.com/KMKfw/boards). Você
precisará dos arquivos `kb.py` e `main.py`. Instruções mais avançadas podem ser
vistas [aqui](config_and_keymap.md).

Note que recomendamos utilizar [KMKPython](https://github.com/KMKfw/kmkpython)
para essas placas pois ele é otimizado para elas. Se você usar o Circuitpython
em vez do KMKPython, você também vai precisar do
[boot.py](https://github.com/KMKfw/kmk_firmware/blob/master/boot.py).

### Você obteve outro teclado, possivelmente artesanal, e quer customizar o KMK para ele

Primeiro, certifique-se de entender como o seu teclado funciona, e em particular
sua configuração matricial específica. Você pode observar
[aqui](http://pcbheaven.com/wikipages/How_Key_Matrices_Works/) ou ler o
[guia](https://docs.qmk.fm/#/hand_wire) feito pelo time da QMK para teclados
artesanais.

<br>Uma vez que você compreendeu a essência da coisa:
- Você pode dar uma olhada [aqui](config_and_keymap.md) e [aqui](keys.md) para
  começar a customizar seu arquivo code.py / main.py.
- Eis uma [referência](keycodes.md) dos códigos de teclas (*keycodes*)
  disponíveis.
- A extensão [internacional](international.md) acrescenta teclas para layouts
  não-americanos, e as [teclas de mídia](media_keys.md) acrecentam teclas
  para... mídia.

E para ir mais além:

- [Sequências](sequences.md) são usadas para enviar múltiplas teclas em uma ação
  só.
- [Camadas](layers.md) podem transformar totalmente como seu teclado age com um
  simples toque.
- [ModTap](modtap.md) te permite customizar a maneira que uma tecla age quando é
  pressionada ou "segurada"; e o
- [TapDance](tapdance.md) dependendo do número de vezes que ela é pressionada.

Você quer extensões divertidas como RGB, teclados repartidos ao meio e mais?
Confira o que os [módulos](modules.md) e [extensões](extensions.md) podem
fazer!

Você também pode obter ideias dos vários [exemplos de
usuários](https://github.com/KMKfw/user_keymaps) que fornecemos e fuce nossa
[documentação](https://github.com/KMKfw/kmk_firmware/tree/master/docs).

<br>

## Ajuda e Suporte Adicionais
> Estradas? Para onde vamos, estradas são desnecessárias.

Caso precise, ajuda para depuração pode ser encontrada [aqui](debugging.md).

Se você precisa de suporte com o KMK ou quer somente dizer oi, encontre-nos no
canal [#kmkfw:klar.sh no Matrix](https://matrix.to/#/#kmkfw:klar.sh). Este canal
tem uma ponte no Discord
[aqui](https://discordapp.com/widget?id=493256121075761173&theme=dark) por
conveniência. Se você precisa de ajuda ou pretende abrir um bug report, se
possível forneça o hash SHA do *commit* utilizado, o qual pode ser obtido
executando este comando no REPL de seu controlador:

`from kmk.consts import KMK_RELEASE;  print(KMK_RELEASE)`
