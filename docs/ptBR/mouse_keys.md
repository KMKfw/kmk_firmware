# Teclas de Mouse

Para habilitar as teclas de mouse e/ou cursor para o teclado, adicione este
módulo à lista:

```python
from kmk.modules.mouse_keys import MouseKeys
keyboard.modules.append(MouseKeys())
```

# Keycodes

|-----------------|------------------------------------------|
| Keycode         | Descrição                                |
|-----------------|------------------------------------------|
| MB_LMB          | Botão esquerdo do mouse                  |
| MB_RMB          | Botão direito do mouse                   |
| MB_MMB          | Botão do meio do mouse                   |
| MW_UP           | Rolar o scroll para cima                 |
| MW_DOWN, MW_DN  | Rolar o scroll para baixo                |
| MS_UP           | Mover o cursor do mouse para cima        |
| MS_DOWN, MS_DN  | Mover o cursor do mouse para baixo       |
| MS_LEFT, MS_LT  | Mover o cursor do mouse para a esquerdax |
| MS_RIGHT, MS_RT | Mover o cursor do mouse para a direita   |
|-----------------|------------------------------------------|

