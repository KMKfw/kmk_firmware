# Instruções para Gravação

Em geral nós recomendamos seguir as instruções no `README.md`, porém,
majoritariamente como artefato de desenvolvimento, outro método de gravar o KMK
existe. Este método é testado e suportado apenas no Linux, porém ele deve
funcionar no MacOS, BSDs e outros Unix-likes. Pode ser que funcione também em
Cygwin e no Windows Subsystem for Linux.

Dado que se tenham disponíveis o `make` e `rsync` no seu sistema (via `$PATH`),
o seguinte copiará a árvore `kmk` para seu dispositivo CircuitPython, bem como o
arquivo definido como `USER_KEYMAP` como seu `main.py`. Ele também copiará o
`boot.py`, que aloca um tamanho de pilha maior que o padrão do CircuitPython
(simplificando - mais RAM do seu dispositivo ficará disponível para o KMK e para
a configuração do seu teclado). Se qualquer destes arquivos já existir no seu
dispositivo CircuitPython, ele será sobrescrito sem aviso algum.

Se você estiver tendo problemas com erros de permissão aqui, **não execute make
como root ou via sudo. Leia a seção a seguir sobre resolução de problemas.

```sh
make MOUNTPOINT=/media/CIRCUITPY USER_KEYMAP=user_keymaps/nameofyourkeymap.py BOARD=board/nameofyourboard/kb.py
```

# Resolvendo Problemas

## Linux/BSD

Confira se seu drive foi montado em algum lugar mediante um aplicativo gráfico
ou algum sistema de auto-montagem. A maioria destas ferramentas monta os
dispositivos em pastas `/media` ou `/run/media`, provavelmente como
`/media/CIRCUITPY`. Se o dispositivo não está montado, você pode ler sobre como
montar um drive manualmente [na
ArchWiki](https://wiki.archlinux.org/index.php/File_systems#Mount_a_file_system).

Por exemplo:

`sudo mount -o uid=$(id -u),gid=$(id -g) /dev/disk/by-label/CIRCUITPY ~/mnt`

Se você ainda está tendo algum problema, confira nossa página de suporte para
saber aonde você pode entrar em contato, e a comunidade irá te ajudar.
