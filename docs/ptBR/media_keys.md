# Teclas de Mídia

A extensão de teclas de mídia acrescenta teclas para controles comuns de
mídia. Ela pode ser adicionada à lista de extensões.

```python
from kmk.extensions.media_keys import MediaKeys
keyboard.extensions.append(MediaKeys())
```

 ## Keycodes

| Tecla                   | Alternativa | Descrição                |
|-------------------------|-------------|--------------------------|
| `KC.AUDIO_MUTE`         | `KC.MUTE`   | Mudo                     |
| `KC.AUDIO_VOL_UP`       | `KC.VOLU`   | Aumenta o Volume         |
| `KC.AUDIO_VOL_DOWN`     | `KC.VOLD`   | Aumenta o Volume         |
| `KC.MEDIA_NEXT_TRACK`   | `KC.MNXT`   | Faixa Seguinte (Windows) |
| `KC.MEDIA_PREV_TRACK`   | `KC.MPRV`   | Faixa Anterior (Windows) |
| `KC.MEDIA_STOP`         | `KC.MSTP`   | Stop Faixa (Windows)     |
| `KC.MEDIA_PLAY_PAUSE`   | `KC.MPLY`   | Tocar/Pausar Faixa       |
| `KC.MEDIA_EJECT`        | `KC.EJCT`   | Ejetar (macOS)           |
| `KC.MEDIA_FAST_FORWARD` | `KC.MFFD`   | Faixa Seguinte (macOS)   |
| `KC.MEDIA_REWIND`       | `KC.MRWD`   | Faixa Anterior (macOS)   |
