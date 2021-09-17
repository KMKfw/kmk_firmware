# Configurando KMK

KMK é configurado mediante uma enorme classe Python da velha guarda chamada
`KMKKeyboard`. Existem subclasses desta configuração que já vem com padrões
previamente preenchidos para diversos teclados conhecidos (por exemple, muitos
teclados QMK, TMK ou ZMK são suportados com um nice!nano, ou mediante nosso
adaptador de pinagem ItsyBitsy-para-ProMicro). Esta classe é a interface
principal entre usuários finais e os funcionamentos internos do KMK. Vamos
mergulhar!

- Edite ou crie um arquivo chamado `main.py` em nosso drive `CIRCUITPY`. Você
  também pode manter este arquivo em seu computador (possivelmente dentro de
  `user_keymaps` - sinta-se livre para submeter um PR com suas definições de
  layout!) e copie-o (seja manualmente, ou se você é adepto de ferramentas de
  desenvolvimento e linha de comando, usando nosso
  [Makefile](https://github.com/KMKfw/kmk_firmware/blob/master/docs/flashing.md)).
  Definitivamente é recomendado que você mantenha uma cópia extra de segurança
  em algum lugar que não o micro-controlador - chips pifam, Circuitpython pode
  ter problemas de corrupção. ou você pode estar em um dia ruim e apagar o
  arquivo errado.

- Atribuir uma instância `KMKKeyboard` a uma variável, por exemplo, `keyboard =
  KMKKeyboard()` (note os parênteses).

- Certificar-se quie esta instância de `KMKKeyboard` é realmente executada ao
fim do arquivo usando um bloco como este:

```python
if __name__ == '__main__':
    keyboard.go()
```

- Atribuir os pinos e a orientação do diodo (necessário apenas em teclados
  artesanais), por exemplo:

```python
import board

from kmk.matrix import DiodeOrientation

col_pins = (board.SCK, board.MOSI, board.MISO, board.RX, board.TX, board.D4)
row_pins = (board.D10, board.D11, board.D12, board.D13, board.D9, board.D6, board.D5, board.SCL)
rollover_cols_every_rows = 4
diode_orientation = DiodeOrientation.COL2ROW
```

Os pinos devem ser baseados naquilo que o CircuitPython chama de pinos na sua
placa particular. Você pode encontrá-los na REPL do seu dispositivo
CircuitPython:

```python
import board
print(dir(board))
```

> Note: `rollover_cols_every_rows` só é suportado com
> `DiodeOrientation.COLUMNS`/`DiodeOrientation.COL2ROW`, não `DiodeOrientation.ROWS`/`DiodeOrientation.ROW2COL`. Este é usado em
> placas como a Planck Rev6 que reusa pinos de coluna para simular uma matriz
> 4x12 na forma de uma matriz 8x6.

- Importe a lista global de definições com `from kmk.keys import KC`. Você pode
  ou exibi-la no REPL como fizemos acima com `board`, ou simplesmente olhar na
  nossa
  [documentação](https://github.com/KMKfw/kmk_firmware/blob/master/docs/keycodes.md).
  Tentamos manter a lista razoavelmente atualizada, mas se tiver algo faltando,
  você pode ter que ler o arquivo-fonte `kmk/keys.py` (e daí abrir um ticket
  para nos avisar que os documentos estão desatualizados, ou mesmo abrir um PR
  ajustando os documentos!)

- Definir um keymap, que é, em termos Python, uma lista de listas de objetos
  `Key`. Um keymap bem simples, para um teclado com apenas duas teclas físicas
  em apenas uma camada, teria essa aparência:

```python
keyboard.keymap = [[KC.A, KC.B]]
```

Você pode definir um monte de outras coisas

- `keyboard.debug_enabled` que vai atirar um monte de informação de depuração
  para o console serial. Raramente isso é necessário, mas pode fornecer
  informação verdadeiramente valiosa se você precisa abrir um ticket.

- `keyboard.tap_time` que define quanto tempo `KC.TT` e `KC.LT` vão esperar
  antes de condiderar uma tecla "segurada" (veja `layers.md`).
