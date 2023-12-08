## Comparação de Firmware

### KMKPython

KMKPython é um *fork* do Circuitpython, mas com bibliotecas para a maior parte
das extensões já embutidas. Isto te poupa de ter que reuni-las e atualizá-las
manualmente. Pode haver outras características adicionadas no futuro exclusivas
para o KMKPython. Para o nice!nano, o KMKPython é altamente recomendado e usado
em lugar do Circuitpython.

#### Diferenças Notáveis

- Bibliotecas embutidas para Bluetooth, RGB etc.
- Economiza espaço, pois os binários gerados são otimizados para teclados.
- micro-controladores como o nice!nano poderão acessar todas as vantagens
  diretamente.

### Circuitpython

Circuitpython pode ser instalado seguindo [este
guia](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython).
É recomendável utilizar a versão mais recente, 5.0 ou superior. Versões beta
podem funcionar, mas espere suporte limitado.

#### Diferenças Notáveis

- Suporta mais dispositivos.
- Menos bibliotecas embutidas. Se precisar de RGB, Bluetooth e mais, você terá
  que adicionar estas bibliotecas manualmente.
- Alguns dispositivos como o nice!nano não dispõem de muito espaço livre, então
  nem todas as vantagens podem ser instaladas ao mesmo tempo.
