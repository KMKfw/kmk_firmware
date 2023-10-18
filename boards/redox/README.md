# ReDox

![Top View](https://github.com/mattdibi/redox-keyboard/raw/master/img/redox-1.jpg)

The ReDox project is a split bodied, column staggered, *Printed Circuit Board* (PCB) design orientated, mechanical keyboard.  
Inspired by the ErgoDox keyboard, designer [Mattia Dal Ben](mailto:matthewdibi@gmail.com)'s main goal was to reduce the physical size of the ErgoDox without lowering key count key drastically, hence **Re**duced Ergo**dox**.   

Hardware Availability: [PCB & Case Data](https://github.com/mattdibi/redox-keyboard)

Extensions enabled by default  
- [Layers](/docs/en/layers.md)
- [MouseKeys](/docs/en/mouse_keys.md)
- [HoldTap](/docs/en/holdtap.md)

## Microcontroller Support

If microcontrollers are not 0xCB Helios:  
In `kb.py` file, replace `helios` with a supported microcontroller listed in `kmk/quickpin/pro_micro`:
```python
from kmk.quickpin.pro_micro.helios import pinout as pins
```
For example, nice!nano controller(s): 
```python
from kmk.quickpin.pro_micro.nice_nano import pinout as pins
```
