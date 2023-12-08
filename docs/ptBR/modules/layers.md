# Camadas

O módulo de camadas acrescenta teclas para acessar outras camadas. Ele pode ser
acrescentado à lista de extensões.



```python
from kmk.modules.layers import Layers
keyboard.modules.append(Layers())
```

## Keycodes

| Tecla               | Descrição                                                                 |
|---------------------|---------------------------------------------------------------------------|
| `KC.DF(layer)`      | Troca a camada padrão                                                     |
| `KC.MO(layer)`      | Ativa a camada momentaneamente, desativa quando solta                     |
| `KC.LM(layer, mod)` | Como `MO(layer)` ,as com `mod` ativo                                      |
| `KC.LT(layer, kc)`  | Ativa a camada momentaneamente se segurada, envia `kc` se tocada          |
| `KC.TG(layer)`      | Habilita a camada se estiver ativa, desativa caso contrário (*toggle*)    |
| `KC.TO(layer)`      | Ativa a camada, desativando todas as outras                               |
| `KC.TT(layer)`      | Ativa a camada momentaneamente se segurada, troca se tocada repetidamente |
