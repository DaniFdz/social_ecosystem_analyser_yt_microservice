# TFG

## Setup CI/CD
```bash
# Create ssh key and add it to folder ~/.ssh/authorized_keys
ssh-keygen -t rsa -b 4096 -f ~/.ssh/droplet_tfg
cat ~/.ssh/droplet_tfg.pub

ssh root@<ip> -i ~/.ssh/droplet_tfg
###
# Create a key to clone the repo from github and it to personal ssh-keys
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub
```

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

- [ ] Pasar ToDo's a trello

- [ ] CI/CD
    - [ ] Migrar tests a pytest
    - [ ] Arreglar tests y coverage
    - [ ] Añadir variables de entorno a github (youtube, cohere y virustotal)
    - [X] Setup DigitalOcean droplet
    - [ ] Descargar docker compose
    - [ ] Setup Cronjobs
        https://www.airplane.dev/blog/docker-cron-jobs-how-to-run-cron-inside-containers

- [X] Firmar anexo 3 Claúsula 2
    - [ ] Confirmar con Chema que está bien

- [X] Cambiar our_exit()
- [X] Migrar a poetry
- [X] Recibir comentarios del vídeo
- [X] Recibir subtitulos?(OAuth2)

- [X] Verificar idioma

- [X] Temas de privacidad, eliminar datos sensibles

- [ ] Interfaz de usuario ( Astro )

- [ ] Echarle un ojo:
    - https://www.phishtool.com/
    - https://www.notta.ai/en/blog/transcribe-youtube-video

- [ ] Instagram / Twitter api investigar free capabilities

- [ ] Análisis sentimientos comentarios (Objetivo NO guardar comentarios)

- [ ] Categorizar por tipos de amenaza
- [ ] Buscar indicadores de peligrosidad

- [ ] Visualizar posibles problemas de ciberseguridad
    https://github.com/apexcharts/apexcharts.js

- [ ] Eliminar algunos contenidos (niños, drogras, etc...) definirlos claramente

- [ ] Caso de uso, este vídeo tiene indicios de amenaza

- [ ] Borrador con decisiones de diseño y requisitos
- [ ] Incluir contenido con respecto a la busqueda de otras redes sociales en dos paginas

- [ ] Roles:
    Sysadmin
    Curador de contenidos
    Usuario proactivo (input: URL; output: malignidad)
    |-> El mismo?
    Usuario analista de datos: (input: palabra, criterio output: grafo con pesos)

- [ ] Crear un modelo de datos
- [ ] Preprocesado de los datos

- [ ] Crear un modelo de clasificación
- [ ] Entrenar el modelo
- [ ] Evaluar el modelo
