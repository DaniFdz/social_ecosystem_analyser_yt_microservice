# TFG

## Installation

### Install [🤖 Just](https://github.com/casey/just) and [🌐 Poetry](https://python-poetry.org/)

```bash
sudo apt install cargo pipx
cargo install just
pipx install poetry
```

### Add cargo bin to path

Add this line to your .bashrc or .zshrc

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

Install dependencies
```bash
just install
```

## ToDo's

- [ ] Firmar anexo 3 Claúsula 2
- [ ] Cambiar our_exit()

- [ ] Migrar a poetry
- [X] Recibir comentarios del vídeo
- [ ] Recibir subtitulos?(OAuth2)

- [X] Verificar idioma

- [ ] Temas de privacidad, eliminar datos sensibles, crear identificador único para cada usuario

- [ ] Como sabemos a dónde nos redirige el vídeo?

    - Crawler que recorra la web alojada en la url y las urls que contenga la web recursivamente (No es legal)

- [ ] Crear un modelo de datos

- [ ] Preprocesado de los datos

- [ ] Crear un modelo de clasificación
- [ ] Entrenar el modelo
- [ ] Evaluar el modelo

- [ ] Interfaz de usuario
