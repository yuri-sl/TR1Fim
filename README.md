# Bem-Vindo ao Simulador SimulNet!


## Descrição do projeto
- Este é um programa que simula o funcionamento de um sistema de transmissão
e recepção de dados.

- Este programa funciona com o uso de sockets e threads.

## Como rodar o programa:
## Importante! Para que a aplicação rode, é necessário que você esteja com algumas bibliotecas instaladas! Para rodá-lo, baixe:
- Para rodar no Ubunto é preciso instalar:
```bash
pip install matplotlib
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-gtk-3.0
```
- Para rodar no Windows é preciso instalar:
```bash
winget install MSYS2.MSYS2 (ou instala normal)
*adiciona c:/msys64/ucrt64/bin e c:/msys64/usr/bin para o PATH
pacman -Suy
pacman -S mingw-w64-ucrt-x86_64-toolchain
pacman -S mingw-w64-ucrt-x86_64-python-gobject
pacman -S mingw-w64-ucrt-x86_64-gtk3
pacman -S mingw-w64-ucrt-x86_64-python
pacman -S mingw-w64-ucrt-x86_64-python-matplotlib
```

- Para inicializar o programa basta rodar
```bash
python notebook.py
```
- No caso do Windows, assegure de usar o python instalado na pasta c:/msys64/ucrt64/bin