# KMK Hardware: Dispositivos para Uso Com KMK

## Adaptador de Pinagem de Itsy Bitsy para Pro Micro

Esta placa adapta a pinagem de uma [Adafruit Itsy Bitsy M4
Express](https://www.adafruit.com/product/3800) compatível com o CircuitPython
para aquela da [Sparkfun Pro Micro](https://www.sparkfun.com/products/12640) a
fim de permitir que a Itsy Bitsy seja usável com os diversos teclados que
suportam a planta do Pro Micro.

## Mapeamento dos Pinos

| Pro Micro | Itsy Bitsy |
|-----------|------------|
| TX0/PD3   | TX         |
| RX1/PD2   | RX         |
| GND       | GND        |
| GND       | GND        |
| 2/PD1     | SDA        |
| 3/PD0     | SCL        |
| 4/PD4     | D13        |
| 5/PC6     | D12        |
| 6/PD7     | D11        |
| 7/PE6     | D10        |
| 8/PB4     | D9         |
| 9/PB5     | D7         |
| Raw       |            |
| GND       | GND        |
| RST       | RST        |
| VCC       | USB        |
| A3/PF4    | A0         |
| A2/PF5    | A1         |
| A1/PF6    | A2         |
| A0/PF7    | A3         |
| 15/PB1    | A4         |
| 14/PB3    | A5         |
| 16/PB2    | SCK        |


## Então como eu uso isso?

1. Os contatos da planta do Pro Micro são circuladas na parte inferior da
   placa. Solde os cabeçotes-macho nestes contatos por baixo da placa (o mesmo
   lado das marcas) de forma que os pinos estendam-se "para baixo" para que
   possam ser plugados no teclado.

2. Os contatos restantes são para a Itsy Bitsy. Asssumindo que a altura seja uma
   preocupação, em vez de soldar os cabeçotes-macho na Itsy Bitsy e os
   cabeçotes-fêmea na placa adaptadora, coloque o lado longo dos cabeçotes-macho
   ao longo dos contatos da Itsy Bitsy por baixo da placa de forma que eles
   projetem-se ao longo dos contatos no topo da placa e soldá-los no
   lugar. Certifique-se de manter os cabeçotes perpendiculares à superfície da
   placa.

3. Uma vez soldados, coloque a placa Itsy Bitsy acima dos cabeçotes que agora
   estão ressaltando para cima de forma que os cabeçalhos passem pelas pads do
   Itsy Bitsy e soldem no lugar.

4. Apare os cabeçotes do Itsy Bits o quanto for necessário com um nivelador.


## Licença, Direitos de Cópia, e Detalhes Jurídicos

Os arquivos deste diretório estão licenciados pela [CC BY-SA
4.0](https://tldrlegal.com/license/creative-commons-attribution-sharealike-4.0-international-(cc-by-sa-4.0))
onde o resumo está ligado, cujo texto completo está no arquivo `LICENSE.md`
neste diretório.
