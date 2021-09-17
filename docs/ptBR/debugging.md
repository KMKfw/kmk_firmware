# Depuração

A depuração liberará a maior parte do estado útil para o console. Isso pode ser
habilitado no seu firmware atribuindo esta configuração em seu teclado. **Note**
que isto o tornará mais lento, portanto habilite somente quando precisar depurar.

```python
keyboard.debug_enabled = True
```

A saída pode ser vista conectando-se à porta serial do teclado. Remeta-se a
[este
documento](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console)
para mais informações sobre conectar-se à porta serial. Para usuários Linux,
recomendamos [picocom](https://github.com/npat-efault/picocom) ou
[screen](https://www.gnu.org/software/screen/manual/screen.html).
