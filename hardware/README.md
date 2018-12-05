# KMK Hardware: Devices for use with KMK

## Itsy Bitsy to Pro Micro pinout adapter

This board adapts the pinout of a Circuit Python compatible [Adafruit Itsy Bitsy M4 Express](https://www.adafruit.com/product/3800) to that of the [Sparkfun Pro Micro](https://www.sparkfun.com/products/12640) to allow the Itsy Bitsy to be used with the many keyboards that support the footprint of the Pro Micro. 

## Pin mapping
Pro Micro Pin | Itsy Bitsy Pin
------------ | -------------
TX0/PD3 | TX
RX1/PD2 | RX
GND | GND
GND | GND
2/PD1 | SDA
3/PD0 | SCL
4/PD4 | D13
5/PC6 | D12
6/PD7 | D11
7/PE6 | D10
8/PB4 | D9
9/PB5 | D7
Raw | 
GND | GND
RST | RST
VCC | USB
A3/PF4 | A0
A2/PF5 | A1
A1/PF6 | A2
A0/PF7 | A3
15/PB1 | A4
14/PB3 | A5
16/PB2 | SCK


## So how do I use it?
1. The pads for the Pro Micro footprint are circled on the underside of the board. Solder male headers into these pads on the underside of the board (the same side as the markings) so that the pins extend "downward" so that they can be plugged into the keyboard.

2. The remaining pads are for the Itsy Bitsy. Assuming height is a concern, rather than soldering male headers into the Itsy Bitsy and female headers into the adapter board, instead place the long side of male headers through the Itsy Bitsy pads from underneath the board so that they protrude through he pads on the top of the board and solder them in place. Make sure to keep the headers perpindicular to the surface of the board.

3. Once soldered, place the Itsy Bitsy board over the headers that are now protruding upwards so that the headers go through the pads of the ItsyBitsy and solder in place.

4. Trim the ItsyBitsy headers as needed with flush cutters.

## License, Copyright, and Legal

The files in this directory are licensed 
[CC BY-SA 4.0](https://tldrlegal.com/license/creative-commons-attribution-sharealike-4.0-international-(cc-by-sa-4.0))
while the tl;dr is linked, the full license text is included in `LICENSE.md` in this directory.
