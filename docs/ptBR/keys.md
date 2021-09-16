# Teclas

> NOTE: Isto não é uma tabela de busca de objetos fornecidos pelo KMK. Esta
> listagem pode ser encontrada em `keycodes.md`. Possivelmente vale a pena
> observar o código-fonte bruto se você estiver travado: `kmk/keys.py`.

Este é um montante de documentação sobre como teclas físicas são mapeada para
eventos (e o ciclo-de-vida destes eventos) no KMK. É um tanto técnico, mas se
você cogita estender a funcionalidade so seu teclado com código extra, você
precisará de pelo menos uma fração deste conhecimento técnico.

Os primeiros passos neste processo não são tão interessantes para a maior parte
dos fluxos de trabalho, razão pela qual eles estão tão soterrados no KMK:
varremos um monte de faixas de GPIO (o quão rápido o CircuitPython nos permitir)
para ver onde, numa matriz de teclas, uma delas foi pressionada. Os detalhes
técnicos deste processo estão melhor descritos na
[Wikipedia](https://en.wikipedia.org/wiki/Keyboard_matrix_circuit). Então,
varremos o mapa de teclas definido, encontrando a primeira tecla válida neste
índice baseado na pilha de camadas ativas (esta lógica, se você quer ler o
código, está em `kmk/internal_state.py`, método `_find_key_in_map`).

Os próximos passos são a parte interessante, mas para compreendê-los precisamos
entender um pouco do objeto `Key` (encontrado em `kmk/keys.py`). Objetos `Key`
têm algumas peças fundamentais de informação:

* O `code`, que pode ser qualquer inteiro. Inteiros menores que
  `FIRST_KMK_INTERNAL_KEY` são enviados pela pilha de HID (e portanto para o
  computador, que traduzirá aquele inteiro para algo útil - por exemplo,
  `code=4` torna-se `a` em um teclado US QWERTY/Dvorak)

* Os modificadores anexados (para implementar coisas como Shift ou `KC.HYPR` que
  são pressionamentos de teclas singulares enviadas juntamente a mais de uma
  tecla em um único reporte HID. Este é um conceito diferente de Sequências, que
  são uma característica do KMK documentada em `sequences.md`). Para todos os
  propósitos fora do núcleo do KMK, este campo deve ser ignorado - ele pode ser
  seguramente populado mediante meios bem mais sãos que perder tempo fazendo
  isso na mão.

* Alguns dados sobre se a tecla deveria ter sido pressionada ou liberada - isto
  é majoritariamente um detalhe de implementação sobre como Sequências
  funcionam, onde, por exemplo, `KC.RALT` pode precisar ser segurada por toda a
  duração da sequência, em vez de ser liberada imediatamente antes de mover para
  o próximo catactere. Geralmente usuários finais não precisam se preocupar com
  isso, mas os campos são denominados `no_press` e `no_release` e são
  referenciados em alguns lugares da base de código se você precisar de
  exemplos.

* Manipuladores (*handler*) para o pressionamento (algumas vezes chamado de
  "keydown" ou "press") e liberação (algumas vezes chamado de "keyup" ou
  "release"). KMK fornece manipuladores para funções padrão do yteclado e
  algumas teclas especiais de sobrescrita (como `KC.GESC`, que é uma forma
  aprimorada de teclas ANSI já existentes) em `kmk/handlers/stock.py`, para
  troca de camadas em `kmk/handlers.layers.py`, e para tudo relacionado a
  sequências (veja de novo `sequences.md`) em
  `kmk/handlers/sequences.py`. Discutiremos mais estes em breve.

* Chamadas de retorno (*callback*) opcionais a serem executadas antes e/ou
  depois dos handlers acima. Mais sobre isso em breve.

* Um campo `meta` genérico, que é mais comumente utilizado para teclas "com
  argumentos" - objetos no objeto `KC` que na realidade são funções que retornam
  instâncias de `Key`, que geralmente precisam acessar os argumentos passados
  para a "função mais externa". Muitos destes exemplos são relacionados com
  trocas de camadas - por exemplo, `KC.MO` é implementada como uma tecla com
  argumentos - quando o usuário acrescenta `KC.MO(1)` ao teclado, a chamada de
  função retorna um objeto `Key` com `meta` contendo um objeto contendo as
  propriedades `layer` e `kc`. Existem outros usos para o campo `meta`, e
  exemplos podem ser encontrados em `kmk/types.py`.

Objetos `Key` também podem ser encadeados chamando eles! Para criar uma tecla
que segura Ctrl e Shift simultaneamente, simplesmente fazemos:

```python
CTRLSHFT = KC.LCTL(KC.LSFT)

keyboard.keymap = [ ... CTRLSHFT ... ]
```

Quando uma tecla é pressionada e tiramos um objeto `Key` do keymap, acontecerá o
seguinte:

- Callbacks pré-pressionamento serão executados na ordem em que foram
  atribuídos, com seus valores de retorno descartados (a não ser que o usuário
  os anexe, eles quase nunca existem).
- O handler de pressionamento correspondente será executado (mais comumente este
  é fornecido pelo KMK).
- Calllbacks pós-pressionamento serão executados na ordem em que foram
  atribuídos, com seus valores de retorno descartados (a não ser que o usuário
  os anexe, eles quase nunca existem).

Os mesmos passos são executados quando uma tecla é liberada.

_OK, então... Mas o que é um handler, e o que são esses callbacks?!_

Grosso modo, todos eles servem a um mesmo propósiti: fazer algo com os dados da
tecla, ou executar efeitos colaterais. A maioria dos handlers são fornecidos
pelo KMK internamente e modificam o `InternalState` de alguma forma -
adicionando a tecla à fila HID, modificando camadas, etc. Os handlers
pré/pós-pressionamento são projetados para permitir que a funcionalidade seja
embutida nestes pontos no fluxo de eventos sem ter que reimplementar (ou
importar e chamar internamente) os handlers internos.

Todos esses métodos recebem os mesmos argumentos, e por isso eu vou copiar a
docstring direto do código-fonte:

> Recebe o seguinte:
>
> - self (Esta instância Key)
> - state (InternalState corrente)
> - KC (A tabela de busca KC, para conveniência)
> - `coord_int` (Um inteiro, representação interna da coordenada da matriz para
>   a tecla pressionada - costumeiramente isto não é útil para usuários finais,
>   mas é fornecida por consistência com os manipuladores internos)
> - `coord_raw` (Uma tupla X,Y de coordenadas da matrix - costumeiramente não é
>   útil, também)
>
> O valor de retorno do callback fornecido é descartado. _Exceções não são
> capturadas_, e provavelmente quebrarão o KMK se não forem tratadas dentro da
> tua função.
>
> Estes handlers são executados na ordem de anexação: handlers fornecidos por
> chamadas anteriores deste método são executados antes daqueles fornecidos por
> chamadas posteriores.

Isto significa que se você quer adicionar coisas como suporte a LED/brilho, ou
um botão que aciona seu modem GSM para falar com alguém, ou seja lá o que você
puder fazer em CircuitPython, que também retenha as capacidades de troca de
camadas ou seja lá qual for o handler de suporte, você está coberto. Isto também
significa que você pode adicionar funcionalidades completamente novas ao KMK
escrevendo seu próprio handler.

Eis um exemplo de gancho de ciclo de vida (*lifecycle hook*) que imprime um
Shrek gigante em Arte ASCII. Ele não utiliza os argumentos que recebe, porque
não tem intenção de modificar o estado interno. Ele é puramente um efeito
colateral ([side
effect](https://en.wikipedia.org/wiki/Side_effect_(computer_science))) executado
sempre que se pressiona o Alt esquerdo:

```python
def shrek(*args, **kwargs):
    print('⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆')
    print('⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿')
    print('⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀')
    print('⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀')
    print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉')


KC.LALT.before_press_handler(shrek)
```

Você também pode copiar uma tecla sem quaisquer handlers pré ou pós nela
mediante `.clone()`, tal que por exemplo, se eu já adicionei Shrek ao meu `LALT`
mas quero um `LALT` sem Shrek em algum lugar do keymap, eu posso simplesmente
clonar a tecla, e a nova tecla não terá meus handlers atrelados a ela:

```python
SHREKLESS_ALT = KC.LALT.clone()
```
